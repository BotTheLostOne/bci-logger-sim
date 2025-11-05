"""
EEG Pattern Generator Module
=============================

Generates synthetic EEG (Electroencephalography) patterns including:
- Standard frequency bands (delta, theta, alpha, beta, gamma)
- Noise patterns
- Event-related potentials (ERPs)
"""

import numpy as np
from typing import Dict, List, Optional, Tuple


class EEGGenerator:
    """
    Generates synthetic EEG patterns for BCI simulation.
    
    Simulates different brain wave frequencies and patterns.
    """
    
    # Standard EEG frequency bands (Hz)
    BANDS = {
        "delta": (0.5, 4),
        "theta": (4, 8),
        "alpha": (8, 13),
        "beta": (13, 30),
        "gamma": (30, 100)
    }
    
    def __init__(self, sampling_rate: float = 250.0, seed: Optional[int] = None):
        """
        Initialize the EEG generator.
        
        Args:
            sampling_rate: Sampling rate in Hz (default: 250 Hz)
            seed: Random seed for reproducibility
        """
        self.sampling_rate = sampling_rate
        self.rng = np.random.RandomState(seed)
    
    def generate_band(
        self,
        band_name: str,
        duration: float,
        amplitude: float = 1.0
    ) -> np.ndarray:
        """
        Generate EEG signal for a specific frequency band.
        
        Args:
            band_name: Name of frequency band ('delta', 'theta', 'alpha', 'beta', 'gamma')
            duration: Duration in seconds
            amplitude: Signal amplitude in microvolts
            
        Returns:
            EEG signal array
        """
        if band_name not in self.BANDS:
            raise ValueError(f"Unknown band: {band_name}")
        
        freq_min, freq_max = self.BANDS[band_name]
        n_samples = int(duration * self.sampling_rate)
        t = np.arange(n_samples) / self.sampling_rate
        
        # Use multiple frequencies within the band
        n_components = 3
        frequencies = self.rng.uniform(freq_min, freq_max, n_components)
        phases = self.rng.uniform(0, 2 * np.pi, n_components)
        weights = self.rng.uniform(0.5, 1.0, n_components)
        weights /= weights.sum()
        
        signal = np.zeros(n_samples)
        for freq, phase, weight in zip(frequencies, phases, weights):
            signal += weight * np.sin(2 * np.pi * freq * t + phase)
        
        return amplitude * signal
    
    def generate_mixed_signal(
        self,
        duration: float,
        band_weights: Optional[Dict[str, float]] = None,
        noise_level: float = 0.1
    ) -> np.ndarray:
        """
        Generate mixed EEG signal with multiple frequency bands.
        
        Args:
            duration: Duration in seconds
            band_weights: Dictionary of band names to weights (default: equal weights)
            noise_level: Amplitude of background noise
            
        Returns:
            Mixed EEG signal array
        """
        if band_weights is None:
            band_weights = {band: 1.0 for band in self.BANDS.keys()}
        
        # Normalize weights
        total_weight = sum(band_weights.values())
        band_weights = {k: v / total_weight for k, v in band_weights.items()}
        
        n_samples = int(duration * self.sampling_rate)
        signal = np.zeros(n_samples)
        
        # Add each frequency band
        for band_name, weight in band_weights.items():
            if weight > 0:
                band_signal = self.generate_band(band_name, duration, amplitude=weight)
                signal += band_signal
        
        # Add background noise
        if noise_level > 0:
            noise = self.rng.normal(0, noise_level, n_samples)
            signal += noise
        
        return signal
    
    def generate_erp(
        self,
        duration: float,
        peak_latency: float,
        peak_amplitude: float = 5.0,
        width: float = 0.1
    ) -> np.ndarray:
        """
        Generate event-related potential (ERP).
        
        Args:
            duration: Duration in seconds
            peak_latency: Time of peak response in seconds
            peak_amplitude: Amplitude of the peak
            width: Width of the ERP waveform
            
        Returns:
            ERP signal array
        """
        n_samples = int(duration * self.sampling_rate)
        t = np.arange(n_samples) / self.sampling_rate
        
        # Gaussian-like ERP
        erp = peak_amplitude * np.exp(-((t - peak_latency) ** 2) / (2 * width ** 2))
        
        return erp
    
    def generate_mental_state(
        self,
        state: str,
        duration: float
    ) -> np.ndarray:
        """
        Generate EEG pattern characteristic of a mental state.
        
        Args:
            state: Mental state ('relaxed', 'focused', 'drowsy', 'active')
            duration: Duration in seconds
            
        Returns:
            EEG signal array
        """
        state_profiles = {
            "relaxed": {"alpha": 3.0, "theta": 1.0, "beta": 0.5, "delta": 0.5, "gamma": 0.2},
            "focused": {"beta": 3.0, "gamma": 2.0, "alpha": 0.5, "theta": 0.3, "delta": 0.2},
            "drowsy": {"delta": 3.0, "theta": 2.0, "alpha": 0.5, "beta": 0.2, "gamma": 0.1},
            "active": {"beta": 2.0, "gamma": 2.5, "alpha": 1.0, "theta": 0.5, "delta": 0.3}
        }
        
        if state not in state_profiles:
            raise ValueError(f"Unknown state: {state}")
        
        return self.generate_mixed_signal(duration, state_profiles[state], noise_level=0.2)
    
    def generate_channel_data(
        self,
        channel_name: str,
        duration: float,
        state: str = "active",
        noise_level: float = 0.1
    ) -> dict:
        """
        Generate complete EEG data for a single channel with metadata.
        
        Args:
            channel_name: Name of the EEG channel (e.g., 'Fp1', 'C3')
            duration: Duration in seconds
            state: Mental state to simulate
            noise_level: Background noise level
            
        Returns:
            Dictionary with EEG data and metadata
        """
        signal = self.generate_mental_state(state, duration)
        n_samples = len(signal)
        time_array = np.arange(n_samples) / self.sampling_rate
        
        return {
            "channel_name": channel_name,
            "signal": signal.tolist(),
            "time": time_array.tolist(),
            "sampling_rate": self.sampling_rate,
            "duration": duration,
            "n_samples": n_samples,
            "state": state,
            "mean_amplitude": float(np.mean(np.abs(signal))),
            "peak_amplitude": float(np.max(np.abs(signal)))
        }
    
    def generate_montage(
        self,
        channel_names: List[str],
        duration: float,
        state: str = "active"
    ) -> List[dict]:
        """
        Generate EEG data for multiple channels (montage).
        
        Args:
            channel_names: List of channel names
            duration: Duration in seconds
            state: Mental state to simulate
            
        Returns:
            List of channel data dictionaries
        """
        montage_data = []
        
        for channel in channel_names:
            channel_data = self.generate_channel_data(channel, duration, state)
            montage_data.append(channel_data)
        
        return montage_data
