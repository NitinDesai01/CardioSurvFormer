"""CatBoost model implementation"""

from catboost import CatBoostRegressor, CatBoostClassifier
import numpy as np
from typing import Dict, Any, Optional
import logging
import pickle

logger = logging.getLogger(__name__)

class CatBoostSurvivalModel:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
    
    def fit(self, X: np.ndarray, y: np.ndarray, time: np.ndarray = None):
        """Fit CatBoost model"""
        self.model = CatBoostRegressor(
            iterations=self.config.get("iterations", 1000),
            learning_rate=self.config.get("learning_rate", 0.05),
            depth=self.config.get("depth", 6),
            l2_leaf_reg=self.config.get("l2_leaf_reg", 3),
            loss_function='RMSE',
            verbose=False,
            random_seed=self.config.get("random_seed", 42)
        )
        
        self.model.fit(X, y)
        logger.info("CatBoost model fitted successfully")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not fitted")
        return self.model.predict(X)
    
    def get_feature_importance(self) -> np.ndarray:
        """Get feature importance"""
        if self.model is None:
            raise ValueError("Model not fitted")
        return self.model.feature_importances_
    
    def save_model(self, filepath: str):
        """Save model to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model from disk"""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        logger.info(f"Model loaded from {filepath}")