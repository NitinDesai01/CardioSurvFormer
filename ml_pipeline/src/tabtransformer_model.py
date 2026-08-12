"""TabTransformer model implementation"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class FeatureEmbedding(nn.Module):
    def __init__(self, categorical_cardinalities: List[int], numerical_dim: int, embedding_dim: int = 64):
        super().__init__()
        self.categorical_embeddings = nn.ModuleList([
            nn.Embedding(cardinality, embedding_dim)
            for cardinality in categorical_cardinalities
        ])
        self.numerical_projection = nn.Linear(numerical_dim, embedding_dim)
        self.embedding_dim = embedding_dim
    
    def forward(self, categorical_features, numerical_features):
        cat_embeddings = []
        for i, embedding in enumerate(self.categorical_embeddings):
            cat_embeddings.append(embedding(categorical_features[:, i].long()))
        
        num_embedding = self.numerical_projection(numerical_features)
        all_embeddings = cat_embeddings + [num_embedding]
        embedded = torch.stack(all_embeddings, dim=1)
        return embedded

class PositionalEncoding(nn.Module):
    def __init__(self, embedding_dim: int, max_len: int = 100):
        super().__init__()
        pe = torch.zeros(max_len, embedding_dim)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, embedding_dim, 2).float() * (-np.log(10000.0) / embedding_dim))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))
    
    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

class TabTransformer(nn.Module):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.embedding_dim = config.get('embedding_dim', 64)
        self.num_heads = config.get('num_heads', 4)
        self.num_layers = config.get('num_layers', 3)
        self.ff_dim = config.get('ff_dim', 128)
        self.dropout = config.get('dropout', 0.1)
        
        self.num_categorical = config.get('num_categorical', 8)
        self.num_numerical = config.get('num_numerical', 3)
        self.categorical_cardinalities = config.get('categorical_cardinalities', [2] * self.num_categorical)
        
        self.embedding = FeatureEmbedding(
            categorical_cardinalities=self.categorical_cardinalities,
            numerical_dim=self.num_numerical,
            embedding_dim=self.embedding_dim
        )
        
        self.pos_encoding = PositionalEncoding(self.embedding_dim)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.embedding_dim,
            nhead=self.num_heads,
            dim_feedforward=self.ff_dim,
            dropout=self.dropout,
            activation='gelu',
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=self.num_layers)
        self.layer_norm = nn.LayerNorm(self.embedding_dim)
        
        self.output_head = nn.Sequential(
            nn.Linear(self.embedding_dim, self.embedding_dim // 2),
            nn.ReLU(),
            nn.Dropout(self.dropout),
            nn.Linear(self.embedding_dim // 2, 1)
        )
    
    def forward(self, categorical_features, numerical_features):
        embedded = self.embedding(categorical_features, numerical_features)
        embedded = self.pos_encoding(embedded)
        transformer_output = self.transformer(embedded)
        transformer_output = self.layer_norm(transformer_output)
        pooled = transformer_output.mean(dim=1)
        output = self.output_head(pooled)
        return output
    
    def get_embeddings(self, categorical_features, numerical_features):
        embedded = self.embedding(categorical_features, numerical_features)
        return embedded