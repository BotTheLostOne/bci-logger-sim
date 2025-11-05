"""
Brain Model Example
===================

Demonstrates using the BrainModel class to simulate AI brain activity.
"""

import sys
import os

# Add parent directory to path to import bci_logger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bci_logger import BrainModel, JSONLogger


def main():
    print("=" * 60)
    print("BCI Logger Simulator - Brain Model Example")
    print("=" * 60)
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Initialize brain model
    print("\n1. Initializing brain model...")
    brain = BrainModel(
        n_neurons=100,
        eeg_channels=['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4'],
        sampling_rate=250.0,
        seed=42
    )
    print(f"   Created brain model with {brain.n_neurons} neurons")
    print(f"   EEG channels: {', '.join(brain.eeg_channels)}")
    
    # Simulate different mental states
    print("\n2. Simulating different mental states...")
    
    states = ["relaxed", "focused", "drowsy", "active"]
    json_logger = JSONLogger(output_dir="output", filename="brain_model_example.json")
    
    for state in states:
        print(f"\n   Simulating '{state}' state...")
        activity = brain.simulate_activity(
            duration=2.0,
            state=state,
            spike_rate_range=(10.0, 50.0)
        )
        
        total_spikes = sum(s['spike_count'] for s in activity['spike_trains'])
        avg_firing_rate = total_spikes / activity['duration'] / brain.n_neurons
        
        print(f"      Total spikes: {total_spikes}")
        print(f"      Average firing rate: {avg_firing_rate:.2f} Hz")
        
        # Log activity
        json_logger.log(activity)
    
    # Get summary statistics
    print("\n3. Brain model summary statistics:")
    stats = brain.get_summary_stats()
    print(f"   Total simulations: {stats['total_simulations']}")
    print(f"   Total duration: {stats['total_duration']:.2f} seconds")
    print(f"   Total spikes: {stats['total_spikes']}")
    print(f"   Average firing rate: {stats['average_firing_rate']:.2f} Hz")
    
    print("\n   State breakdown:")
    for state, data in stats['states'].items():
        print(f"      {state}: {data['count']} simulations, {data['duration']:.2f}s total")
    
    # Save logs
    json_path = json_logger.save()
    print(f"\n4. Saved logs to: {json_path}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
