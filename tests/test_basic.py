"""
Basic tests for BCI Logger Simulator
=====================================

Simple smoke tests to verify core functionality.
"""

import sys
import os
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bci_logger import (
    SpikeGenerator,
    EEGGenerator,
    BrainModel,
    JSONLogger,
    CSVLogger,
    IntuitionRollAPI
)


def test_spike_generator():
    """Test spike train generation."""
    gen = SpikeGenerator(seed=42)
    
    # Test Poisson spikes
    spikes = gen.poisson_spikes(rate=20.0, duration=1.0)
    assert len(spikes) > 0, "Should generate spikes"
    assert all(0 <= t <= 1.0 for t in spikes), "Spike times should be in duration"
    
    # Test spike train generation
    train = gen.generate_spike_train(neuron_id=1, rate=20.0, duration=1.0)
    assert train['neuron_id'] == 1
    assert 'spike_times' in train
    assert 'firing_rate' in train
    
    # Test population
    pop = gen.generate_population(n_neurons=10, rate_range=(10.0, 30.0), duration=1.0)
    assert len(pop) == 10
    
    print("✓ Spike generator tests passed")


def test_eeg_generator():
    """Test EEG signal generation."""
    gen = EEGGenerator(sampling_rate=250.0, seed=42)
    
    # Test band generation
    signal = gen.generate_band('alpha', duration=1.0)
    assert len(signal) == 250, "Should have correct number of samples"
    
    # Test mixed signal
    mixed = gen.generate_mixed_signal(duration=1.0)
    assert len(mixed) == 250
    
    # Test mental state
    state_signal = gen.generate_mental_state('focused', duration=1.0)
    assert len(state_signal) == 250
    
    # Test channel data
    channel = gen.generate_channel_data('C3', duration=1.0)
    assert channel['channel_name'] == 'C3'
    assert 'signal' in channel
    assert 'time' in channel
    
    print("✓ EEG generator tests passed")


def test_brain_model():
    """Test brain model simulation."""
    brain = BrainModel(n_neurons=50, seed=42)
    
    # Test activity simulation
    activity = brain.simulate_activity(duration=1.0, state='active')
    assert 'spike_trains' in activity
    assert 'eeg_signals' in activity
    assert activity['n_neurons'] == 50
    
    # Test intuition signal
    intuition = brain.generate_intuition_signal(difficulty=15, character_wisdom=12)
    assert 'intuition_data' in intuition
    assert 'spike_trains' in intuition
    assert 'eeg_signals' in intuition
    
    # Test summary stats
    stats = brain.get_summary_stats()
    assert stats['total_simulations'] > 0
    
    print("✓ Brain model tests passed")


def test_loggers():
    """Test logging functionality."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test JSON logger
        json_logger = JSONLogger(output_dir=tmpdir, filename="test.json")
        json_logger.log({"test": "data"})
        path = json_logger.save()
        assert os.path.exists(path)
        
        loaded = json_logger.load()
        assert len(loaded) == 1
        assert loaded[0]['test'] == 'data'
        
        # Test CSV logger
        csv_logger = CSVLogger(output_dir=tmpdir, filename="test.csv")
        spike_data = [{
            'neuron_id': 1,
            'spike_times': [0.1, 0.2, 0.3],
            'spike_count': 3,
            'duration': 1.0,
            'firing_rate': 3.0,
            'mode': 'poisson'
        }]
        csv_path = csv_logger.save_spike_trains(spike_data)
        assert os.path.exists(csv_path)
    
    print("✓ Logger tests passed")


def test_intuition_api():
    """Test intuition roll API."""
    with tempfile.TemporaryDirectory() as tmpdir:
        brain = BrainModel(n_neurons=20, seed=42)
        api = IntuitionRollAPI(brain_model=brain, enable_logging=True, log_dir=tmpdir)
        
        # Test single check
        result = api.intuition_check(
            character_name="TestChar",
            wisdom=15,
            difficulty=12,
            context="test"
        )
        
        assert 'character_name' in result
        assert 'intuition_check' in result
        assert 'neural_summary' in result
        
        # Test callback registration
        callback_called = []
        def test_callback(data):
            callback_called.append(data)
        
        api.register_callback("post_roll", test_callback)
        api.intuition_check("TestChar2", wisdom=10, difficulty=10)
        assert len(callback_called) > 0
        
        # Test statistics
        stats = api.get_statistics()
        assert stats['total_checks'] >= 2
    
    print("✓ Intuition API tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running BCI Logger Simulator Tests")
    print("=" * 60)
    print()
    
    test_spike_generator()
    test_eeg_generator()
    test_brain_model()
    test_loggers()
    test_intuition_api()
    
    print()
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
