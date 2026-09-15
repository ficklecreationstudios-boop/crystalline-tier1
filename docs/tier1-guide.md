# Tier 1 Setup Guide

## Quick Start

### Installation

This repository is currently documented and validated as a source distribution; it does not make a public PyPI availability claim.

From a local checkout:

```bash
git clone https://github.com/ficklecreationstudios-boop/crystalline-tier1.git
cd crystalline-tier1
pip install .
```

For development, including development dependencies:

```bash
pip install -e ".[dev]"
```

### Basic Usage

```python
from crystalline import spectral_analysis
import numpy as np

t = np.linspace(0, 10, 1000)
signal = np.sin(2 * np.pi * 1.5 * t) + 0.5 * np.sin(2 * np.pi * 3 * t)
frequencies, psd = spectral_analysis(signal, fs=100.0)
print(f"Max frequency: {frequencies[np.argmax(psd)]:.2f} Hz")
```

## Scope

Crystalline Tier 1 is a free, CPU-only Python package built on NumPy and SciPy.

| Capability | Tier 1 |
|---|---:|
| Spectral analysis | Yes |
| Signal filtering | Yes |
| Linear algebra | Yes |
| GPU acceleration | No |
| JIT specialization | No |
| Domain-specific wheels | No |
| Commercial/enterprise features | No |

This guide does not assign prices or performance targets to higher tiers because those capabilities are outside this repository and are not validated by its code or benchmark suite.

## Numerical conventions

### Spectral analysis

`spectral_analysis` returns a one-sided, density-scaled PSD. Its documented numerical convention is aligned with SciPy's periodogram behavior for the same window, with `detrend=False` and `scaling='density'`.

### Filtering

`spectral_filtering` uses SciPy's digital Butterworth filter and `filtfilt`. Because the public API does not accept a sampling-frequency argument, `cutoff` is normalized: values must be strictly between `0` and `1`, where `1` is Nyquist.

For example:

```python
filtered = spectral_filtering(signal, cutoff=0.2, order=4, btype="low")
filtered = spectral_filtering(signal, cutoff=[0.1, 0.4], order=4, btype="band")
```

## Backend

```python
from crystalline import get_backend

backend = get_backend()
print(backend.device)        # cpu
print(backend.gpu_available) # False
print(backend.tier)          # TIER_1_FREE
```

Attempts to select a GPU or another unavailable tier raise `TierFeatureBlockedError`.

## Convolution

The CPU backend supports one-dimensional convolution with optional zero padding and positive integer stride:

```python
result = backend.convolution(signal, kernel, padding=1, stride=2)
```

The implementation uses SciPy's `signal.convolve(..., mode='same')` and then selects every `stride`-th output.

## Examples

### Spectral analysis

```python
from crystalline import spectral_analysis

fs = 1000
t = np.arange(0, 1, 1/fs)
signal = np.sin(2*np.pi*50*t) + 0.5*np.sin(2*np.pi*120*t)
freqs, power = spectral_analysis(signal, fs=fs)
peaks = np.argsort(power)[-2:]
print("Dominant frequencies:", freqs[peaks])
```

## Troubleshooting

### Feature not available in Tier 1

GPU and other higher-tier features are intentionally unavailable in this distribution. Use the CPU API exposed by this repository.

### ImportError

Install the package from a local source checkout as described above, or install its runtime dependencies directly when working without an installed package:

```bash
pip install numpy scipy
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md).

## Support

- **Issues:** https://github.com/ficklecreationstudios-boop/crystalline-tier1/issues
- **Source:** https://github.com/ficklecreationstudios-boop/crystalline-tier1

## Next Steps

- Read [API Reference](./api-reference.md)
- Explore [Examples](../examples/)
- Review the independent numerical tests under `tests/`
