"""Explainability utilities"""

import numpy as np
import shap
import matplotlib.pyplot as plt
from typing import Dict, Any, Optional

class Explainability:
    def __init__(self, model):
        self.model = model
        self.explainer = None
    
    def create_shap_explainer(self, X_background):
        """Create SHAP explainer"""
        if hasattr(self.model, 'predict'):
            self.explainer = shap.TreeExplainer(self.model)
        else:
            self.explainer = shap.DeepExplainer(self.model, X_background)
        return self.explainer
    
    def get_shap_values(self, X):
        """Get SHAP values for predictions"""
        if self.explainer is None:
            raise ValueError("Explainer not created. Call create_shap_explainer first.")
        return self.explainer.shap_values(X)
    
    def plot_shap_summary(self, shap_values, X, feature_names):
        """Create SHAP summary plot"""
        shap.summary_plot(shap_values, X, feature_names=feature_names)
        plt.tight_layout()
    
    def plot_feature_importance(self, shap_values, feature_names):
        """Create feature importance plot"""
        shap.summary_plot(shap_values, feature_names=feature_names, plot_type="bar")
        plt.tight_layout()