# Contributing to Crystalline GPU - Tier 1

Thank you for your interest in contributing to Crystalline GPU Tier 1! This is an open-source project under GPL-3.0.

## How to Contribute

### Reporting Bugs

1. Check [existing issues](https://github.com/yourusername/crystalline-tier1/issues)
2. Create a new issue with:
   - Clear title
   - Description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS

### Suggesting Improvements

1. Create an issue with the `enhancement` label
2. Describe the improvement and why it's needed
3. Discuss with maintainers before implementing

### Submitting Code

1. **Fork** the repository
2. **Branch** off `main`: `git checkout -b feature/my-feature`
3. **Make changes** following coding standards below
4. **Test** your changes: `pytest tests/`
5. **Commit** with clear messages: `git commit -m "Add feature X"`
6. **Push** to your fork
7. **Create Pull Request** with description

## Coding Standards

### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4-space indentation
- Maximum line length: 100 characters
- Use `black` for formatting: `black .`
- Use `flake8` for linting: `flake8 .`

### Documentation
- Add docstrings to all functions and classes
- Use Google-style docstrings
- Include examples where helpful

### Example:
```python
def spectral_analysis(data, fs=None, window='hamming'):
    """Perform spectral analysis using FFT.
    
    Args:
        data: Input signal (numpy array)
        fs: Sampling frequency (default: 1.0)
        window: Window function (default: 'hamming')
        
    Returns:
        Tuple of (frequencies, power_spectral_density)
        
    Example:
        >>> freqs, psd = spectral_analysis(data, fs=100.0)
    """
```

### Testing
- Write tests for all new features
- Run tests: `pytest`
- Aim for >80% coverage: `pytest --cov`
- Tests go in `tests/test_*.py`

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/crystalline-tier1.git
cd crystalline-tier1

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Check linting
black --check .
flake8 .
```

## Important: Tier 1 Restrictions

This is a **free, open-source Tier 1** project. When contributing:

✅ **DO:**
- Keep features CPU-based (no GPU code)
- Use NumPy, SciPy, Python stdlib only
- Maintain GPL-3.0 license compliance
- Document tier restrictions clearly
- Help improve core algorithms

❌ **DON'T:**
- Add GPU code or CUDA dependencies
- Add commercial licensing code
- Include code from higher tiers
- Remove tier enforcement checks
- Violate GPL-3.0 terms

## Commit Message Guidelines

```
[Type] Brief description (50 chars max)

Longer explanation if needed (wrap at 72 chars).
Explain WHAT and WHY, not HOW.

- Bullet point for additional detail
- Another detail point

Fixes #123
```

Types:
- `[FEAT]` - New feature
- `[FIX]` - Bug fix
- `[DOCS]` - Documentation
- `[STYLE]` - Code style (no logic change)
- `[TEST]` - Add/update tests
- `[REFACTOR]` - Refactor code

## Code Review

All PRs require review before merging. Reviewers will check:

- Code quality and style
- Test coverage
- Documentation completeness
- Tier 1 policy compliance
- Performance implications

## License

By contributing, you agree that your contributions will be licensed under GPL-3.0.

## Questions?

- Open an issue
- Start a discussion
- Email: contact@crystalline.io

---

**Thank you for contributing to Crystalline GPU Tier 1!** 🎉
