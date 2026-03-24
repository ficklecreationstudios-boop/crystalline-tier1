# Tier 1 Setup Guide

## Quick Start

### Installation

```bash
pip install crystalline-tier1
```

### Basic Usage

```python
from crystalline import get_backend, spectral_analysis
import numpy as np

# Generate sample data
t = np.linspace(0, 10, 1000)
signal = np.sin(2 * np.pi * 1.5 * t) + 0.5 * np.sin(2 * np.pi * 3 * t)

# Perform spectral analysis
frequencies, psd = spectral_analysis(signal, fs=100.0)

# Print results
print(f"Max frequency: {frequencies[np.argmax(psd)]:.2f} Hz")
```

## Understanding Tiers

### This is Tier 1 (Free, CPU-only)

Crystalline GPU is organized into four tiers:

| Feature | Tier 1 (This) | Tier 2 | Tier 3 | Tier 4 |
|---------|---------------|--------|---------|---------|
| **Cost** | Free | $500/mo | $100K+/yr | $300K+/yr |
| **GPU** | ❌ | ✅ | ✅ | ✅ |
| **Speedup** | N/A | 20-100x | 50-500x | 100-3000x |
| **Champion Mode** | ❌ | ❌ | ❌ | ✅ |
| **JIT Specialization** | ❌ | ❌ | ❌ | ✅ |
| **Domain Wheels** | ❌ | ❌ | ✅ | ✅ |
| **Support** | Community | Professional | Enterprise | Premium |

### What You Get in Tier 1

✅ **Included:**
- Spectral analysis (FFT-based)
- Signal processing (filtering, convolution)
- Linear algebra (matrix ops, solve)
- Open-source GPL-3.0 license
- CPU-only (no GPU)
- Full source code
- Community support

❌ **Not Included:**
- GPU acceleration (Tier 2+)
- Champion Mode optimization (Tier 4)
- JIT specialization (Tier 4)
- Domain-specific wheels (Tier 3+)
- Commercial licensing
- Enterprise support

## Security & Isolation

This Tier 1 package includes built-in safeguards to prevent unauthorized access to higher-tier features:

1. **Tier Enforcement**: All features are checked against Tier 1 permissions at runtime
2. **Feature Blocking**: Any attempt to access GPU or higher-tier features raises `TierFeatureBlockedError`
3. **.gitignore Protection**: Higher-tier files are excluded from Git to prevent mixing
4. **License Validation**: Disabled for open-source Tier 1 (no licensing system)

### Attempting Forbidden Features

If you try to access higher-tier features:

```python
from crystalline.backend import GPUBackend

# This will raise TierFeatureBlockedError
backend = GPUBackend()  # ERROR: GPU not available in Tier 1
```

Error message:
```
TierFeatureBlockedError: GPU acceleration is not available in Tier 1 (free edition). 
For GPU support, please upgrade to Tier 2+. 
Contact [CONTACT_EMAIL]
```

## Examples

### 1. Basic Spectral Analysis

```python
from crystalline import spectral_analysis
import numpy as np

# Create a multi-frequency signal
fs = 1000  # Sample rate 1 kHz
t = np.arange(0, 1, 1/fs)
signal = (
    np.sin(2*np.pi*50*t) +           # 50 Hz
    0.5*np.sin(2*np.pi*120*t) +      # 120 Hz
    0.25*np.sin(2*np.pi*250*t)       # 250 Hz
)

# Analyze
freqs, power = spectral_analysis(signal, fs=fs)

# Find dominant frequencies
peaks = np.argsort(power)[-3:]
print("Dominant frequencies:", freqs[peaks])
```

### 2. Filtering

```python
from crystalline import spectral_filtering

# Low-pass filter to remove high frequencies
filtered = spectral_filtering(
    signal, 
    cutoff=100,  # Hz
    order=4,
    btype='low'
)
```

### 3. Get Backend

```python
from crystalline import get_backend

backend = get_backend()
print(f"Backend: {backend.device}")
print(f"GPU Available: {backend.gpu_available}")
print(f"Tier: {backend.tier}")
```

## Troubleshooting

### "Feature not available in Tier 1"

**Problem**: You're trying to use GPU or higher-tier features.

**Solution**: These require paid tiers. Contact [CONTACT_EMAIL]

### ImportError

**Problem**: `ModuleNotFoundError: No module named 'crystalline'`

**Solution**:
```bash
pip install crystalline-tier1
# Or for development:
git clone https://github.com/yourusername/crystalline-tier1.git
cd crystalline-tier1
pip install -e .
```

### Dependency Issues

**Problem**: NumPy or SciPy not found.

**Solution**:
```bash
pip install numpy scipy
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/crystalline-tier1/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/crystalline-tier1/discussions)
- **Commercial**: [CONTACT_EMAIL]

## Next Steps

- Read [API Reference](./api-reference.md)
- Explore [Examples](../examples/)
- Join the [Community](link-to-community)
