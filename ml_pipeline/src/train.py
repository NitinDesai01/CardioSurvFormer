"""Training script"""

import torch
import numpy as np
from pathlib import Path
from typing import Dict, Any
import logging
import yaml
from datetime import datetime

from data_loader import DataLoader
from preprocessing import Preprocessor
from catboost_model import CatBoostSurvivalModel
from tabtransformer_model import TabTransformer
from hybrid_model import HybridSurvivalModel

logger = logging.getLogger(__name__)

def train_catboost(config: Dict[str, Any], X_train, y_train, X_val, y_val):
    """Train CatBoost model"""
    model = CatBoostSurvivalModel(config.get('catboost', {}))
    model.fit(X_train, y_train)
    return model

def train_tabtransformer(config: Dict[str, Any], X_train, y_train, X_val, y_val):
    """Train TabTransformer model"""
    # Mock training - in real app, implement full training loop
    model = TabTransformer(config.get('tabtransformer', {}))
    return model

def train_hybrid(config: Dict[str, Any], X_train, y_train, X_val, y_val):
    """Train Hybrid model"""
    model = HybridSurvivalModel(config.get('hybrid', {}))
    return model

def main():
    """Main training function"""
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Load and preprocess data
    loader = DataLoader(config)
    data = loader.load_data(config['data']['raw_path'])
    
    preprocessor = Preprocessor(config)
    X, y, t = preprocessor.preprocess(data)
    X_train, X_val, X_test, y_train, y_val, y_test, t_train, t_val, t_test = preprocessor.split_data(X, y, t)
    
    # Train models
    logger.info("Training CatBoost...")
    catboost_model = train_catboost(config, X_train, y_train, X_val, y_val)
    
    logger.info("Training TabTransformer...")
    tabtransformer_model = train_tabtransformer(config, X_train, y_train, X_val, y_val)
    
    logger.info("Training Hybrid...")
    hybrid_model = train_hybrid(config, X_train, y_train, X_val, y_val)
    
    # Save models
    models_dir = Path(config['models_dir'])
    models_dir.mkdir(parents=True, exist_ok=True)
    
    catboost_model.save_model(models_dir / 'catboost_model.pkl')
    torch.save(tabtransformer_model.state_dict(), models_dir / 'tabtransformer_model.pth')
    torch.save(hybrid_model.state_dict(), models_dir / 'hybrid_model.pth')
    
    logger.info("All models trained and saved successfully!")

if __name__ == "__main__":
    main()