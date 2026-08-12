"""Survival analysis loss functions"""

import torch
import torch.nn.functional as F
import numpy as np

def cox_loss(predictions, time, event):
    """Cox proportional hazards loss"""
    sorted_idx = torch.argsort(time, descending=True)
    predictions = predictions[sorted_idx]
    event = event[sorted_idx]
    risk_set = torch.exp(predictions)
    cumulative_risk = torch.cumsum(risk_set, dim=0)
    loss = -torch.sum(event * (predictions - torch.log(cumulative_risk + 1e-8)))
    return loss

def negative_log_likelihood_survival(predictions, time, event):
    """Negative log likelihood for survival"""
    sorted_idx = torch.argsort(time, descending=True)
    predictions = predictions[sorted_idx]
    event = event[sorted_idx]
    
    risk_set = torch.exp(predictions)
    cumulative_risk = torch.cumsum(risk_set, dim=0)
    
    nll = -torch.sum(event * (predictions - torch.log(cumulative_risk + 1e-8)))
    return nll

def deep_surv_loss(predictions, time, event):
    """DeepSurv loss function"""
    return cox_loss(predictions, time, event)

def rank_loss(predictions, time, event):
    """Rank-based loss for survival prediction"""
    n = len(predictions)
    loss = 0
    count = 0
    
    for i in range(n):
        for j in range(n):
            if event[i] == 1 and time[i] < time[j]:
                loss += torch.max(torch.tensor(0.0), predictions[j] - predictions[i])
                count += 1
    
    return loss / (count + 1e-8)