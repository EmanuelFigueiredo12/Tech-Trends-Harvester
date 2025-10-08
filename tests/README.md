# Tests

Unit tests for Tech Trends Harvester.

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run with coverage:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Run specific test file:
```bash
pytest tests/test_util.py -v
```

### Run specific test:
```bash
pytest tests/test_util.py::test_is_question -v
```

## Test Structure

- `test_util.py` - Tests for utility functions (tokenization, question detection, filtering)
- `test_aggregate.py` - Tests for aggregation and categorization functions

## Adding New Tests

1. Create a new test file: `tests/test_<module>.py`
2. Import the module you want to test
3. Write test functions starting with `test_`
4. Use assertions to verify behavior

Example:
```python
def test_my_function():
    result = my_function("input")
    assert result == "expected output"
```

## CI Integration

All tests run automatically on:
- Every push to main
- Every pull request
- Multiple platforms (Ubuntu, macOS, Windows)
- Multiple Python versions (3.9, 3.10, 3.11, 3.12)

## Coverage

We aim for >80% code coverage. Check coverage with:
```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```
