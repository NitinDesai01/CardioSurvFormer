"""Hybrid CatBoost-TabTransformer model"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class CrossAttentionFusion(nn.Module):
    def __init__(self, dim: int, num_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.cat_to_trans_attn = nn.MultiheadAttention(dim, num_heads, dropout=dropout, batch_first=True)
        self.trans_to_cat_attn = nn.MultiheadAttention(dim, num_heads, dropout=dropout, batch_first=True)
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)
        self.ffn = nn.Sequential(
            nn.Linear(dim * 2, dim * 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(dim * 2, dim)
        )
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, cat_features, trans_features):
        cat_features = cat_features.unsqueeze(1)
        trans_features = trans_features.unsqueeze(1)
        
        cat_attended, _ = self.cat_to_trans_attn(cat_features, trans_features, trans_features)
        cat_attended = self.norm1(cat_features + cat_attended)
        cat_attended = self.dropout(cat_attended)
        
        trans_attended, _ = self.trans_to_cat_attn(trans_features, cat_features, cat_features)
        trans_attended = self.norm2(trans_features + trans_attended)
        trans_attended = self.dropout(trans_attended)
        
        combined = torch.cat([cat_attended.squeeze(1), trans_attended.squeeze(1)], dim=1)
        fused = self.ffn(combined)
        return fused

class SurvivalHead(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64, output_dim: int = 1):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.fc3 = nn.Linear(hidden_dim // 2, output_dim)
        self.dropout = nn.Dropout(0.2)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.bn2 = nn.BatchNorm1d(hidden_dim // 2)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return x

class HybridSurvivalModel(nn.Module):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.catboost_dim = config.get('catboost_dim', 64)
        self.transformer_dim = config.get('transformer_dim', 64)
        self.hidden_dim = config.get('hidden_dim', 64)
        
        self.fusion = CrossAttentionFusion(
            dim=self.catboost_dim,
            num_heads=config.get('num_heads', 4),
            dropout=config.get('dropout', 0.1)
        )
        
        self.survival_head = SurvivalHead(
            input_dim=self.catboost_dim,
            hidden_dim=self.hidden_dim
        )
        
        self.risk_head = nn.Sequential(
            nn.Linear(self.catboost_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        
        self.time_head = nn.Sequential(
            nn.Linear(self.catboost_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1),
            nn.ReLU()
        )
        
        self._initialize_weights()
    
    def _initialize_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
    
    def forward(self, catboost_features, transformer_features, time=None, event=None):
        fused_features = self.fusion(catboost_features, transformer_features)
        survival_output = self.survival_head(fused_features)
        risk_score = self.risk_head(fused_features)
        predicted_time = self.time_head(fused_features)
        
        outputs = {
            'survival_output': survival_output,
            'risk_score': risk_score,
            'predicted_time': predicted_time,
            'fused_features': fused_features
        }
        
        if time is not None and event is not None:
            outputs['survival_loss'] = self._cox_loss(survival_output, time, event)
            outputs['risk_loss'] = F.binary_cross_entropy(risk_score.squeeze(), event.float())
        
        return outputs
    
    def _cox_loss(self, predictions, time, event):
        sorted_idx = torch.argsort(time, descending=True)
        predictions = predictions[sorted_idx]
        event = event[sorted_idx]
        risk_set = torch.exp(predictions)
        cumulative_risk = torch.cumsum(risk_set, dim=0)
        loss = -torch.sum(event * (predictions - torch.log(cumulative_risk + 1e-8)))
        return loss
    
    def predict_risk(self, catboost_features, transformer_features):
        with torch.no_grad():
            outputs = self.forward(catboost_features, transformer_features)
            return outputs['risk_score'].numpy()
    
    def predict_survival(self, catboost_features, transformer_features):
        with torch.no_grad():
            outputs = self.forward(catboost_features, transformer_features)
            risk = outputs['risk_score']
            return 1 - risk.numpy()