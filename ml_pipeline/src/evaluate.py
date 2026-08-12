"""Evaluation script"""

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def concordance_index(predictions, time, event):
    """Calculate concordance index"""
    # Simplified C-index calculation
    n = len(predictions)
    concordant = 0
    comparable = 0
    
    for i in range(n):
        for j in range(n):
            if i != j and event[i] == 1 and event[j] == 1:
                if time[i] < time[j]:
                    if predictions[i] > predictions[j]:
                        concordant += 1
                    comparable += 1
    
    return concordant / (comparable + 1e-8)

def brier_score(predictions, time, event, time_points):
    """Calculate Brier score"""
    # Simplified Brier score calculation
    brier_scores = []
    for t in time_points:
        survival_prob = np.exp(-predictions * t / 365)
        brier = np.mean((event - survival_prob) ** 2)
        brier_scores.append(brier)
    return np.mean(brier_scores)

def evaluate_model(model, X_test, y_test, t_test):
    """Evaluate a model"""
    if hasattr(model, 'predict'):
        predictions = model.predict(X_test)
    else:
        predictions = model(X_test).numpy()
    
    # Classification metrics
    pred_binary = (predictions > 0.5).astype(int)
    metrics = {
        'accuracy': accuracy_score(y_test, pred_binary),
        'precision': precision_score(y_test, pred_binary),
        'recall': recall_score(y_test, pred_binary),
        'f1': f1_score(y_test, pred_binary),
        'roc_auc': roc_auc_score(y_test, predictions),
        'c_index': concordance_index(predictions, t_test, y_test),
        'brier_score': brier_score(predictions, t_test, y_test, [30, 60, 90, 180, 365])
    }
    
    return metrics

def compare_models(models, X_test, y_test, t_test):
    """Compare multiple models"""
    results = {}
    for name, model in models.items():
        logger.info(f"Evaluating {name}...")
        results[name] = evaluate_model(model, X_test, y_test, t_test)
    
    # Create comparison table
    df = pd.DataFrame(results).T
    logger.info("\nModel Comparison:\n" + str(df))
    return df