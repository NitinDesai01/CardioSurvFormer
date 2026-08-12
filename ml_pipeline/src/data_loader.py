"""Data loader for heart failure dataset"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data = None
        self.feature_names = None
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load dataset from CSV"""
        try:
            self.data = pd.read_csv(filepath)
            logger.info(f"Loaded data with {len(self.data)} rows and {len(self.data.columns)} columns")
            self.feature_names = self.data.columns.tolist()
            return self.data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def get_summary(self) -> Dict[str, Any]:
        """Get data summary"""
        if self.data is None:
            return {}
        return {
            "num_samples": len(self.data),
            "num_features": len(self.data.columns),
            "missing_values": self.data.isnull().sum().to_dict(),
            "target_distribution": self.data.get("DEATH_EVENT", pd.Series()).value_counts().to_dict()
        }