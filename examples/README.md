# BCI Logger Simulator - Examples

This folder contains example scripts demonstrating the capabilities of the BCI Logger Simulator.

## Running the Examples

From this directory, run:

```bash
python basic_example.py
python brain_model_example.py
python game_loop_example.py
```

Or from the project root:

```bash
python examples/basic_example.py
```

## Example Descriptions

### basic_example.py

Demonstrates fundamental features:
- Spike train generation (single neuron and populations)
- EEG signal generation (single channel and montages)
- Data logging to JSON and CSV formats

**Output:**
- `output/basic_example.json` - Complete data in JSON format
- `output/spikes_basic.csv` - Spike train data in CSV
- `output/eeg_basic.csv` - EEG signal data in CSV

### brain_model_example.py

Shows how to use the BrainModel class:
- Creating a brain model with multiple neurons and EEG channels
- Simulating different mental states (relaxed, focused, drowsy, active)
- Collecting and analyzing summary statistics
- Logging brain activity data

**Output:**
- `output/brain_model_example.json` - Brain activity logs

### game_loop_example.py

Full neural-DnD game integration demo:
- Setting up a party of adventurers with different wisdom scores
- Running game scenarios with intuition checks
- Neural signal generation for each check
- Callback system for critical successes/failures
- Session statistics and logging

**Output:**
- `output/bci_data_*.json` - Session logs in JSON
- `output/intuition_checks.csv` - Check results in CSV

## Output

All examples create an `output/` directory in the current working directory for their log files. This directory is ignored by git (see `.gitignore`).

## Customization

Each example script can be easily modified to:
- Change neural parameters (firing rates, duration, etc.)
- Adjust EEG sampling rates and channels
- Modify game mechanics (difficulty, wisdom scores)
- Add custom callbacks and logging
- Experiment with different mental states

Feel free to use these examples as templates for your own applications!
