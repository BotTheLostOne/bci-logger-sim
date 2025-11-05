# BCI Logger Simulator

A Brain-Computer Interface (BCI) logger simulator in Python that generates and logs synthetic neural signals (spike trains, EEG patterns) from AI 'brain' models for research and gaming applications.

## Features

- **Spike Train Generation**: Generate realistic neural spike trains using multiple models:
  - Poisson process
  - Refractory period model
  - Burst firing patterns
  
- **EEG Pattern Generation**: Simulate EEG signals with:
  - Standard frequency bands (delta, theta, alpha, beta, gamma)
  - Mental state patterns (relaxed, focused, drowsy, active)
  - Multi-channel montages
  - Event-related potentials (ERPs)

- **AI Brain Model**: High-level interface combining spike and EEG generation to simulate complete brain activity

- **Logging Utilities**: 
  - JSON logger for structured data
  - CSV logger for time series and tabular data
  - Automatic timestamping and metadata

- **Gaming Integration**: API hooks for neural-DnD games with intuition rolls
  - D20-based intuition checks backed by neural signals
  - Callback system for game events
  - Automatic logging of game sessions

## Installation

### Requirements

- Python 3.7+
- NumPy

### Setup

1. Clone the repository:
```bash
git clone https://github.com/BotTheLostOne/bci-logger-sim.git
cd bci-logger-sim
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install in development mode:
```bash
pip install -e .
```

## Quick Start

### Basic Usage

```python
from bci_logger import SpikeGenerator, EEGGenerator, JSONLogger

# Generate spike trains
spike_gen = SpikeGenerator(seed=42)
spike_train = spike_gen.generate_spike_train(
    neuron_id=1,
    rate=20.0,  # 20 Hz firing rate
    duration=5.0,  # 5 seconds
    mode="poisson"
)

# Generate EEG signals
eeg_gen = EEGGenerator(sampling_rate=250.0, seed=42)
eeg_data = eeg_gen.generate_channel_data(
    channel_name="C3",
    duration=5.0,
    state="focused"
)

# Log data
logger = JSONLogger(output_dir="logs")
logger.log({"spikes": spike_train, "eeg": eeg_data})
logger.save()
```

### Brain Model Simulation

```python
from bci_logger import BrainModel

# Create a brain model
brain = BrainModel(
    n_neurons=100,
    eeg_channels=['Fp1', 'Fp2', 'C3', 'C4'],
    sampling_rate=250.0
)

# Simulate brain activity
activity = brain.simulate_activity(
    duration=2.0,
    state="focused",
    spike_rate_range=(10.0, 50.0)
)

# Get summary statistics
stats = brain.get_summary_stats()
print(f"Total simulations: {stats['total_simulations']}")
print(f"Average firing rate: {stats['average_firing_rate']:.2f} Hz")
```

### Neural-DnD Integration

```python
from bci_logger import BrainModel, IntuitionRollAPI

# Initialize API
brain = BrainModel(n_neurons=50)
intuition_api = IntuitionRollAPI(brain_model=brain, enable_logging=True)

# Register callbacks for critical rolls
def on_critical_success(data):
    print(f"🎉 Natural 20 for {data['character_name']}!")

intuition_api.register_callback("critical_success", on_critical_success)

# Perform intuition check
result = intuition_api.intuition_check(
    character_name="Gandalf",
    wisdom=18,
    difficulty=15,
    context="Detect hidden trap"
)

print(f"Roll: {result['intuition_check']['d20_roll']}")
print(f"Success: {result['intuition_check']['success']}")
print(f"Neural state: {result['neural_summary']['state']}")

# Save session logs
intuition_api.save_logs(format="json")
```

## Examples

The `examples/` folder contains complete demonstration scripts:

- **basic_example.py**: Basic spike and EEG generation with logging
- **brain_model_example.py**: Brain model simulation across different mental states
- **game_loop_example.py**: Full neural-DnD game session with intuition rolls

Run an example:
```bash
cd examples
python game_loop_example.py
```

## API Reference

### SpikeGenerator

Generates synthetic neural spike trains.

**Methods:**
- `poisson_spikes(rate, duration, dt)`: Poisson process spike train
- `refractory_spikes(rate, duration, refractory_period, dt)`: Spikes with refractory period
- `burst_spikes(burst_rate, spikes_per_burst, duration, ...)`: Bursting patterns
- `generate_spike_train(neuron_id, rate, duration, mode, **kwargs)`: Complete spike train with metadata
- `generate_population(n_neurons, rate_range, duration, mode)`: Population of neurons

### EEGGenerator

Generates synthetic EEG patterns.

**Methods:**
- `generate_band(band_name, duration, amplitude)`: Single frequency band signal
- `generate_mixed_signal(duration, band_weights, noise_level)`: Mixed multi-band signal
- `generate_erp(duration, peak_latency, peak_amplitude, width)`: Event-related potential
- `generate_mental_state(state, duration)`: State-specific EEG pattern
- `generate_channel_data(channel_name, duration, state, noise_level)`: Complete channel data
- `generate_montage(channel_names, duration, state)`: Multi-channel montage

### BrainModel

High-level AI brain model interface.

**Methods:**
- `simulate_activity(duration, state, spike_rate_range)`: Simulate complete brain activity
- `generate_intuition_signal(difficulty, character_wisdom, duration)`: Gaming-specific intuition signal
- `get_summary_stats()`: Summary statistics of activity history

### IntuitionRollAPI

API for neural-DnD game integration.

**Methods:**
- `register_callback(event, callback)`: Register event callback
- `intuition_check(character_name, wisdom, difficulty, context, duration)`: Perform intuition check
- `batch_intuition_checks(checks)`: Multiple checks in batch
- `save_logs(format)`: Save session logs (JSON or CSV)
- `get_statistics()`: Get session statistics

### Loggers

**JSONLogger:**
- `log(data, add_timestamp)`: Add entry to log
- `save(pretty)`: Save to JSON file
- `save_single(data, filename)`: Save single entry
- `load(filepath)`: Load from JSON file
- `clear()`: Clear log entries

**CSVLogger:**
- `save_spike_trains(spike_data, filename)`: Save spike trains to CSV
- `save_eeg_signals(eeg_data, filename)`: Save EEG signals to CSV
- `save_summary(data, filename)`: Save summary statistics to CSV

## Project Structure

```
bci-logger-sim/
├── bci_logger/           # Main package
│   ├── __init__.py
│   ├── spike_generator.py   # Spike train generation
│   ├── eeg_generator.py     # EEG pattern generation
│   ├── brain_model.py       # AI brain model
│   ├── logger.py            # JSON/CSV logging utilities
│   └── api_hooks.py         # Gaming API hooks
├── examples/             # Example scripts
│   ├── basic_example.py
│   ├── brain_model_example.py
│   └── game_loop_example.py
├── tests/                # Unit tests
├── LICENSE               # MIT License
├── README.md             # This file
└── requirements.txt      # Dependencies
```

## Use Cases

### Research
- Generate synthetic neural data for algorithm development
- Test signal processing pipelines
- Create datasets for machine learning training
- Simulate different brain states and conditions

### Gaming
- Add neural-backed intuition mechanics to RPGs
- Create brain-state dependent gameplay
- Log player "mental" performance
- Build adaptive difficulty systems

### Education
- Teach neuroscience concepts with interactive simulations
- Demonstrate EEG signal processing
- Visualize neural activity patterns
- Explore brain-computer interface concepts

## Contributing

Contributions are welcome! This is an open-core project designed for easy forking and extension.

### Areas for Contribution
- Additional spike generation models
- More EEG patterns and artifacts
- Visualization tools
- More gaming integrations
- Performance optimizations
- Documentation improvements

## License

MIT License - See [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Bot The Lost One

## Acknowledgments

Built for the neural-DnD community and BCI research enthusiasts. Special thanks to the open-source neuroscience community for inspiration.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing examples for common use cases
- Review the API reference above

---

**Happy neural signal generation! 🧠⚡**