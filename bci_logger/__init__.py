"""
BCI Logger Simulator
====================

A Brain-Computer Interface (BCI) logger simulator in Python.
Generates and logs synthetic neural signals (spike trains, EEG patterns)
from AI 'brain' models for research and gaming applications.
"""

__version__ = "0.1.0"
__author__ = "Bot The Lost One"
__license__ = "MIT"

from .spike_generator import SpikeGenerator
from .eeg_generator import EEGGenerator
from .brain_model import BrainModel
from .logger import JSONLogger, CSVLogger
from .api_hooks import IntuitionRollAPI

__all__ = [
    "SpikeGenerator",
    "EEGGenerator",
    "BrainModel",
    "JSONLogger",
    "CSVLogger",
    "IntuitionRollAPI",
]
