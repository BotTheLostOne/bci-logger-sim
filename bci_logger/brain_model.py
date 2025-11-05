"""
AI Brain Model Module
=====================

Combines spike trains and EEG patterns to simulate an AI 'brain' model.
Provides high-level interface for generating neural activity.
"""

import numpy as np
from typing import Dict, List, Optional, Any
from .spike_generator import SpikeGenerator
from .eeg_generator import EEGGenerator


class BrainModel:
    """
    AI Brain Model that generates synthetic neural signals.
    
    Combines spike trains and EEG patterns to simulate brain activity
    for research and gaming applications.
    """
    
    def __init__(
        self,
        n_neurons: int = 100,
        eeg_channels: Optional[List[str]] = None,
        sampling_rate: float = 250.0,
        seed: Optional[int] = None
    ):
        """
        Initialize the brain model.
        
        Args:
            n_neurons: Number of neurons to simulate
            eeg_channels: List of EEG channel names (default: standard 10-20 system subset)
            sampling_rate: EEG sampling rate in Hz
            seed: Random seed for reproducibility
        """
        self.n_neurons = n_neurons
        self.sampling_rate = sampling_rate
        self.seed = seed
        
        # Default EEG channels (subset of 10-20 system)
        if eeg_channels is None:
            self.eeg_channels = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4']
        else:
            self.eeg_channels = eeg_channels
        
        # Initialize generators
        self.spike_gen = SpikeGenerator(seed=seed)
        self.eeg_gen = EEGGenerator(sampling_rate=sampling_rate, seed=seed)
        
        # State tracking
        self.current_state = "active"
        self.activity_history = []
    
    def simulate_activity(
        self,
        duration: float,
        state: str = "active",
        spike_rate_range: tuple = (5.0, 50.0)
    ) -> Dict[str, Any]:
        """
        Simulate brain activity for a given duration.
        
        Args:
            duration: Duration in seconds
            state: Mental state ('relaxed', 'focused', 'drowsy', 'active')
            spike_rate_range: Tuple of (min_rate, max_rate) for spike generation
            
        Returns:
            Dictionary containing spike trains and EEG data
        """
        self.current_state = state
        
        # Generate spike trains for neuron population
        spike_data = self.spike_gen.generate_population(
            self.n_neurons,
            spike_rate_range,
            duration,
            mode="poisson"
        )
        
        # Generate EEG data for all channels
        eeg_data = self.eeg_gen.generate_montage(
            self.eeg_channels,
            duration,
            state
        )
        
        activity = {
            "duration": duration,
            "state": state,
            "spike_trains": spike_data,
            "eeg_signals": eeg_data,
            "n_neurons": self.n_neurons,
            "n_channels": len(self.eeg_channels),
            "sampling_rate": self.sampling_rate,
            "timestamp": None  # Will be set by logger
        }
        
        self.activity_history.append({
            "duration": duration,
            "state": state,
            "spike_count": sum(s["spike_count"] for s in spike_data)
        })
        
        return activity
    
    def generate_intuition_signal(
        self,
        difficulty: int = 10,
        character_wisdom: int = 10,
        duration: float = 1.0
    ) -> Dict[str, Any]:
        """
        Generate neural signals for an 'intuition roll' in gaming context.
        
        Simulates brain activity when a character attempts an intuition check.
        Higher wisdom and lower difficulty produce more 'focused' patterns.
        
        Args:
            difficulty: Difficulty class (DC) of the check (1-30)
            character_wisdom: Wisdom score of the character (1-30)
            duration: Duration of the intuition event in seconds
            
        Returns:
            Dictionary with neural signals and intuition score
        """
        # Calculate intuition score based on difficulty and wisdom
        wisdom_mod = (character_wisdom - 10) // 2
        base_roll = np.random.randint(1, 21)  # D20 roll
        intuition_score = base_roll + wisdom_mod
        success = intuition_score >= difficulty
        
        # Determine brain state based on success
        if success:
            if intuition_score >= difficulty + 5:
                state = "focused"  # Strong success
                spike_rate_range = (30.0, 60.0)
            else:
                state = "active"  # Marginal success
                spike_rate_range = (20.0, 45.0)
        else:
            if intuition_score < difficulty - 5:
                state = "drowsy"  # Critical failure
                spike_rate_range = (5.0, 20.0)
            else:
                state = "relaxed"  # Close failure
                spike_rate_range = (10.0, 30.0)
        
        # Generate neural activity
        activity = self.simulate_activity(duration, state, spike_rate_range)
        
        # Add intuition-specific metadata
        activity["intuition_data"] = {
            "d20_roll": int(base_roll),
            "wisdom_modifier": int(wisdom_mod),
            "total_score": int(intuition_score),
            "difficulty_class": int(difficulty),
            "success": bool(success),
            "character_wisdom": int(character_wisdom)
        }
        
        return activity
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """
        Get summary statistics of the brain model's activity history.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.activity_history:
            return {
                "total_simulations": 0,
                "total_duration": 0.0,
                "states": {}
            }
        
        total_duration = sum(h["duration"] for h in self.activity_history)
        total_spikes = sum(h["spike_count"] for h in self.activity_history)
        
        states = {}
        for h in self.activity_history:
            state = h["state"]
            if state not in states:
                states[state] = {"count": 0, "duration": 0.0}
            states[state]["count"] += 1
            states[state]["duration"] += h["duration"]
        
        return {
            "total_simulations": len(self.activity_history),
            "total_duration": total_duration,
            "total_spikes": total_spikes,
            "average_firing_rate": total_spikes / total_duration if total_duration > 0 else 0,
            "states": states,
            "n_neurons": self.n_neurons,
            "n_channels": len(self.eeg_channels)
        }
