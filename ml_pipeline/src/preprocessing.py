"""Preprocessing pipeline"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)

class Preprocessor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.scaler = StandardScaler()
        self.label_encoders = {}
    
    def preprocess(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Preprocess data"""
        # Separate features and target
        if "DEATH_EVENT" in data.columns:
            X = data.drop(columns=["DEATH_EVENT", "time"])
            y = data["DEATH_EVENT"]
            t = data["time"]
        else:
            X = data
            y = None
            t = None
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Encode categorical features
        categorical_cols = X.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            X[col] = self.label_encoders[col].fit_transform(X[col])
        
        # Scale numerical features
        numerical_cols = X.select_dtypes(include=[np.number]).columns
        X[numerical_cols] = self.scaler.fit_transform(X[numerical_cols])
        
        return X.values, y.values if y is not None else None, t.values if t is not None else None
    
    def split_data(self, X: np.ndarray, y: np.ndarray, t: np.ndarray) -> Tuple:
        """Split data into train/val/test"""
        test_size = self.config.get("test_size", 0.15)
        val_size = self.config.get("val_size", 0.15)
        random_state = self.config.get("random_state", 42)
        
        X_temp, X_test, y_temp, y_test, t_temp, t_test = train_test_split(
            X, y, t,
            test_size=test_size,
            random_state=random_state,
            stratify=y
        )
        
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val, t_train, t_val = train_test_split(
            X_temp, y_temp, t_temp,
            test_size=val_size_adjusted,
            random_state=random_state,
            stratify=y_temp
        )
        
        return X_train, X_val, X_test, y_train, y_val, y_test, t_train, t_val, t_test