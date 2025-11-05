# Tests

Basic test suite for the BCI Logger Simulator.

## Running Tests

From the project root:

```bash
python tests/test_basic.py
```

Or if you have pytest installed:

```bash
pytest tests/
```

## Test Coverage

The test suite covers:
- Spike train generation (Poisson, refractory, burst modes)
- EEG signal generation (bands, mental states, channels)
- Brain model simulation
- JSON and CSV logging
- Intuition roll API and callbacks

## Adding Tests

Additional tests can be added to `test_basic.py` or in new test files following the pattern:

```python
def test_feature_name():
    """Test description."""
    # Test code here
    assert condition, "error message"
    print("✓ Test passed")
```
