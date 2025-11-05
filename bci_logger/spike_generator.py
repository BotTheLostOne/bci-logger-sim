"""
Spike Train Generator Module
=============================

Generates synthetic neural spike trains using various models:
- Poisson process
- Refractory period model
- Burst firing patterns
"""

import numpy as np
from typing import List, Tuple, Optional


class SpikeGenerator:
    """
    Generates synthetic neural spike trains.
    
    Supports multiple generation modes for different neural activity patterns.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the spike generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.rng = np.random.RandomState(seed)
    
    def poisson_spikes(self, rate: float, duration: float, dt: float = 0.001) -> np.ndarray:
        """
        Generate spike train using Poisson process.
        
        Args:
            rate: Firing rate in Hz
            duration: Duration in seconds
            dt: Time step in seconds (default: 1ms)
            
        Returns:
            Array of spike times in seconds
        """
        n_bins = int(duration / dt)
        prob = rate * dt
        spikes = self.rng.random(n_bins) < prob
        spike_times = np.where(spikes)[0] * dt
        return spike_times
    
    def refractory_spikes(
        self, 
        rate: float, 
        duration: float, 
        refractory_period: float = 0.002,
        dt: float = 0.001
    ) -> np.ndarray:
        """
        Generate spike train with refractory period.
        
        Args:
            rate: Target firing rate in Hz
            duration: Duration in seconds
            refractory_period: Absolute refractory period in seconds
            dt: Time step in seconds
            
        Returns:
            Array of spike times in seconds
        """
        spike_times = []
        t = 0.0
        last_spike = -refractory_period
        
        while t < duration:
            if t - last_spike >= refractory_period:
                # Poisson probability adjusted for refractory period
                if self.rng.random() < rate * dt:
                    spike_times.append(t)
                    last_spike = t
            t += dt
        
        return np.array(spike_times)
    
    def burst_spikes(
        self,
        burst_rate: float,
        spikes_per_burst: int,
        duration: float,
        intraburst_interval: float = 0.005,
        dt: float = 0.001
    ) -> np.ndarray:
        """
        Generate bursting spike pattern.
        
        Args:
            burst_rate: Rate of bursts in Hz
            spikes_per_burst: Number of spikes per burst
            duration: Duration in seconds
            intraburst_interval: Time between spikes within burst
            dt: Time step in seconds
            
        Returns:
            Array of spike times in seconds
        """
        # Generate burst onset times
        burst_times = self.poisson_spikes(burst_rate, duration, dt)
        
        spike_times = []
        for burst_start in burst_times:
            for i in range(spikes_per_burst):
                spike_time = burst_start + i * intraburst_interval
                if spike_time < duration:
                    spike_times.append(spike_time)
        
        return np.array(sorted(spike_times))
    
    def generate_spike_train(
        self,
        neuron_id: int,
        rate: float,
        duration: float,
        mode: str = "poisson",
        **kwargs
    ) -> dict:
        """
        Generate a complete spike train with metadata.
        
        Args:
            neuron_id: Identifier for the neuron
            rate: Firing rate in Hz
            duration: Duration in seconds
            mode: Generation mode ('poisson', 'refractory', 'burst')
            **kwargs: Additional parameters for specific modes
            
        Returns:
            Dictionary with spike train data and metadata
        """
        if mode == "poisson":
            spike_times = self.poisson_spikes(rate, duration, **kwargs)
        elif mode == "refractory":
            spike_times = self.refractory_spikes(rate, duration, **kwargs)
        elif mode == "burst":
            spike_times = self.burst_spikes(rate, duration=duration, **kwargs)
        else:
            raise ValueError(f"Unknown mode: {mode}")
        
        return {
            "neuron_id": neuron_id,
            "spike_times": spike_times.tolist(),
            "spike_count": len(spike_times),
            "duration": duration,
            "mode": mode,
            "firing_rate": len(spike_times) / duration if duration > 0 else 0,
            "parameters": kwargs
        }
    
    def generate_population(
        self,
        n_neurons: int,
        rate_range: Tuple[float, float],
        duration: float,
        mode: str = "poisson"
    ) -> List[dict]:
        """
        Generate spike trains for a population of neurons.
        
        Args:
            n_neurons: Number of neurons
            rate_range: Tuple of (min_rate, max_rate) in Hz
            duration: Duration in seconds
            mode: Generation mode for all neurons
            
        Returns:
            List of spike train dictionaries
        """
        population_data = []
        
        for i in range(n_neurons):
            rate = self.rng.uniform(rate_range[0], rate_range[1])
            spike_train = self.generate_spike_train(i, rate, duration, mode)
            population_data.append(spike_train)
        
        return population_data
