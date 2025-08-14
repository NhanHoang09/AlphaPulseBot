"""
Training Module
Module chứa các class và function liên quan đến training LSTM models
"""

from .batch_trainer import BatchTrainer
from .training_manager import TrainingManager

__all__ = ['BatchTrainer', 'TrainingManager']

# Version info
__version__ = '1.0.0'
__author__ = 'AlphaPulseBot Team'
