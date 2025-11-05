"""
Logging Utilities Module
=========================

Provides JSON and CSV logging utilities for BCI data.
"""

import json
import csv
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path


class JSONLogger:
    """
    Logger for saving BCI data in JSON format.
    
    Supports both single-file and multi-file logging modes.
    """
    
    def __init__(self, output_dir: str = "logs", filename: Optional[str] = None):
        """
        Initialize JSON logger.
        
        Args:
            output_dir: Directory for log files
            filename: Base filename (default: timestamped)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bci_data_{timestamp}.json"
        
        self.filepath = self.output_dir / filename
        self.log_entries = []
    
    def log(self, data: Dict[str, Any], add_timestamp: bool = True) -> None:
        """
        Add data entry to log.
        
        Args:
            data: Dictionary containing BCI data
            add_timestamp: Whether to add timestamp to entry
        """
        entry = data.copy()
        
        if add_timestamp:
            entry["timestamp"] = datetime.now().isoformat()
        
        self.log_entries.append(entry)
    
    def save(self, pretty: bool = True) -> str:
        """
        Save logged data to JSON file.
        
        Args:
            pretty: Whether to use pretty printing
            
        Returns:
            Path to saved file
        """
        with open(self.filepath, 'w') as f:
            if pretty:
                json.dump(self.log_entries, f, indent=2)
            else:
                json.dump(self.log_entries, f)
        
        return str(self.filepath)
    
    def save_single(self, data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Save a single data entry to a JSON file.
        
        Args:
            data: Dictionary containing BCI data
            filename: Output filename (default: timestamped)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bci_entry_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(filepath)
    
    def load(self, filepath: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load data from JSON file.
        
        Args:
            filepath: Path to JSON file (default: use instance filepath)
            
        Returns:
            List of data entries
        """
        if filepath is None:
            filepath = self.filepath
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def clear(self) -> None:
        """Clear the current log entries."""
        self.log_entries = []


class CSVLogger:
    """
    Logger for saving BCI data in CSV format.
    
    Optimized for tabular data like spike times and time series.
    """
    
    def __init__(self, output_dir: str = "logs", filename: Optional[str] = None):
        """
        Initialize CSV logger.
        
        Args:
            output_dir: Directory for log files
            filename: Base filename (default: timestamped)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bci_data_{timestamp}.csv"
        
        self.filepath = self.output_dir / filename
    
    def save_spike_trains(self, spike_data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """
        Save spike train data to CSV.
        
        Args:
            spike_data: List of spike train dictionaries
            filename: Output filename (default: use instance filename)
            
        Returns:
            Path to saved file
        """
        if filename:
            filepath = self.output_dir / filename
        else:
            filepath = self.filepath
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'neuron_id', 'spike_time', 'spike_count', 'duration',
                'firing_rate', 'mode'
            ])
            
            # Write spike data
            for neuron in spike_data:
                neuron_id = neuron['neuron_id']
                spike_count = neuron['spike_count']
                duration = neuron['duration']
                firing_rate = neuron['firing_rate']
                mode = neuron['mode']
                
                if neuron['spike_times']:
                    for spike_time in neuron['spike_times']:
                        writer.writerow([
                            neuron_id, spike_time, spike_count, duration,
                            firing_rate, mode
                        ])
                else:
                    # Write one row even if no spikes
                    writer.writerow([
                        neuron_id, None, spike_count, duration,
                        firing_rate, mode
                    ])
        
        return str(filepath)
    
    def save_eeg_signals(self, eeg_data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """
        Save EEG signal data to CSV.
        
        Args:
            eeg_data: List of EEG channel dictionaries
            filename: Output filename (default: use instance filename)
            
        Returns:
            Path to saved file
        """
        if filename:
            filepath = self.output_dir / filename
        else:
            filepath = self.filepath
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'channel_name', 'time', 'amplitude', 'sampling_rate',
                'state', 'mean_amplitude', 'peak_amplitude'
            ])
            
            # Write EEG data
            for channel in eeg_data:
                channel_name = channel['channel_name']
                sampling_rate = channel['sampling_rate']
                state = channel['state']
                mean_amp = channel['mean_amplitude']
                peak_amp = channel['peak_amplitude']
                
                for time, amplitude in zip(channel['time'], channel['signal']):
                    writer.writerow([
                        channel_name, time, amplitude, sampling_rate,
                        state, mean_amp, peak_amp
                    ])
        
        return str(filepath)
    
    def save_summary(self, data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """
        Save summary statistics to CSV.
        
        Args:
            data: List of summary dictionaries
            filename: Output filename (default: use instance filename)
            
        Returns:
            Path to saved file
        """
        if filename:
            filepath = self.output_dir / filename
        else:
            filepath = self.filepath
        
        if not data:
            return str(filepath)
        
        with open(filepath, 'w', newline='') as f:
            # Get all unique keys
            fieldnames = set()
            for entry in data:
                fieldnames.update(entry.keys())
            fieldnames = sorted(fieldnames)
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        return str(filepath)
