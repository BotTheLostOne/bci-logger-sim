"""
Basic BCI Logger Example
=========================

Demonstrates basic usage of the BCI logger simulator:
- Generating spike trains
- Generating EEG patterns
- Logging data to JSON and CSV
"""

import sys
import os

# Add parent directory to path to import bci_logger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bci_logger import SpikeGenerator, EEGGenerator, JSONLogger, CSVLogger


def main():
    print("=" * 60)
    print("BCI Logger Simulator - Basic Example")
    print("=" * 60)
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Initialize generators
    print("\n1. Initializing generators...")
    spike_gen = SpikeGenerator(seed=42)
    eeg_gen = EEGGenerator(sampling_rate=250.0, seed=42)
    
    # Generate spike trains
    print("\n2. Generating spike trains...")
    duration = 5.0  # 5 seconds
    
    # Single neuron spike train
    spike_train = spike_gen.generate_spike_train(
        neuron_id=1,
        rate=20.0,  # 20 Hz
        duration=duration,
        mode="poisson"
    )
    print(f"   Generated {spike_train['spike_count']} spikes for neuron {spike_train['neuron_id']}")
    print(f"   Firing rate: {spike_train['firing_rate']:.2f} Hz")
    
    # Population of neurons
    population = spike_gen.generate_population(
        n_neurons=10,
        rate_range=(10.0, 40.0),
        duration=duration,
        mode="poisson"
    )
    total_spikes = sum(n['spike_count'] for n in population)
    print(f"\n   Generated population of {len(population)} neurons")
    print(f"   Total spikes: {total_spikes}")
    
    # Generate EEG signals
    print("\n3. Generating EEG signals...")
    
    # Single channel
    eeg_channel = eeg_gen.generate_channel_data(
        channel_name="C3",
        duration=duration,
        state="focused"
    )
    print(f"   Generated EEG for channel {eeg_channel['channel_name']}")
    print(f"   Samples: {eeg_channel['n_samples']}")
    print(f"   Mean amplitude: {eeg_channel['mean_amplitude']:.2f} μV")
    
    # Multiple channels (montage)
    channels = ['Fp1', 'Fp2', 'C3', 'C4']
    montage = eeg_gen.generate_montage(
        channel_names=channels,
        duration=duration,
        state="active"
    )
    print(f"\n   Generated montage with {len(montage)} channels")
    
    # Log data
    print("\n4. Logging data...")
    
    # JSON logging
    json_logger = JSONLogger(output_dir="output", filename="basic_example.json")
    json_logger.log({
        "experiment": "basic_example",
        "spike_trains": population,
        "eeg_signals": montage,
        "duration": duration
    })
    json_path = json_logger.save()
    print(f"   Saved JSON log to: {json_path}")
    
    # CSV logging for spike trains
    csv_logger = CSVLogger(output_dir="output")
    csv_spike_path = csv_logger.save_spike_trains(
        population,
        filename="spikes_basic.csv"
    )
    print(f"   Saved spike trains to: {csv_spike_path}")
    
    # CSV logging for EEG signals
    csv_eeg_path = csv_logger.save_eeg_signals(
        montage,
        filename="eeg_basic.csv"
    )
    print(f"   Saved EEG signals to: {csv_eeg_path}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
