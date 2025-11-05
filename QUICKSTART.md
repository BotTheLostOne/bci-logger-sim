# BCI Logger Simulator - Quick Reference

## Installation

```bash
pip install -r requirements.txt
pip install -e .  # For development
```

## Quick Examples

### Generate Spike Trains

```python
from bci_logger import SpikeGenerator

gen = SpikeGenerator(seed=42)
spikes = gen.poisson_spikes(rate=20.0, duration=5.0)
print(f"Generated {len(spikes)} spikes")
```

### Generate EEG Signals

```python
from bci_logger import EEGGenerator

eeg = EEGGenerator(sampling_rate=250.0)
signal = eeg.generate_mental_state("focused", duration=5.0)
```

### Simulate Brain Activity

```python
from bci_logger import BrainModel

brain = BrainModel(n_neurons=100)
activity = brain.simulate_activity(duration=2.0, state="active")
```

### Log Data

```python
from bci_logger import JSONLogger, CSVLogger

# JSON
json_logger = JSONLogger(output_dir="logs")
json_logger.log(activity)
json_logger.save()

# CSV
csv_logger = CSVLogger(output_dir="logs")
csv_logger.save_spike_trains(activity['spike_trains'])
```

### Neural-DnD Integration

```python
from bci_logger import IntuitionRollAPI, BrainModel

brain = BrainModel()
api = IntuitionRollAPI(brain_model=brain)

result = api.intuition_check(
    character_name="Gandalf",
    wisdom=18,
    difficulty=15,
    context="Detect trap"
)

print(f"Roll: {result['intuition_check']['d20_roll']}")
print(f"Success: {result['intuition_check']['success']}")
```

## Module Overview

| Module | Purpose |
|--------|---------|
| `spike_generator.py` | Generate neural spike trains |
| `eeg_generator.py` | Generate EEG signal patterns |
| `brain_model.py` | High-level brain simulation |
| `logger.py` | JSON/CSV logging utilities |
| `api_hooks.py` | Gaming integration API |

## Running Examples

```bash
cd examples
python basic_example.py         # Basic spike/EEG generation
python brain_model_example.py   # Brain model demonstration
python game_loop_example.py     # Neural-DnD game integration
```

## Running Tests

```bash
python tests/test_basic.py
# or with pytest
pytest tests/
```

## Output Files

Examples create an `output/` directory with:
- `*.json` - Structured neural data
- `*.csv` - Time series and tabular data
- Session logs and statistics

## Common Parameters

### Spike Generation
- `rate`: Firing rate in Hz (typically 5-100)
- `duration`: Time in seconds
- `mode`: "poisson", "refractory", or "burst"

### EEG Generation
- `sampling_rate`: Hz (typical: 250-1000)
- `state`: "relaxed", "focused", "drowsy", "active"
- `duration`: Time in seconds

### Brain Model
- `n_neurons`: Number of neurons (typical: 50-1000)
- `eeg_channels`: List of channel names
- `spike_rate_range`: (min_hz, max_hz)

### Intuition Checks
- `wisdom`: Character wisdom score (1-30)
- `difficulty`: DC check value (1-30)
- `duration`: Neural activity duration (0.5-2.0 seconds)

## Tips

1. Use `seed` parameter for reproducible results
2. Output directory is auto-created if it doesn't exist
3. Logs are timestamped automatically
4. CSV format is better for large time series data
5. JSON format preserves complete metadata

## Further Reading

- See `README.md` for full documentation
- Check `examples/` for complete use cases
- Review module docstrings for detailed API info
