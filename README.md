# Crystalline Tier 1

![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)
![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen)
![Platform: Cross-platform](https://img.shields.io/badge/Platform-Cross--platform-lightgrey)

**Open-source CPU numerical and signal-processing utilities for learning, research, and experimentation.**

## Tier 1: CPU-only

Crystalline Tier 1 is the free, open-source edition. It provides a small Python API built on NumPy and SciPy.

### Available

- FFT-based one-sided power spectral density analysis
- Butterworth signal filtering
- CPU linear algebra helpers
- CPU matrix multiplication
- Basic one-dimensional convolution with padding and stride
- Source-visible implementation for research and experimentation

### Not included

- GPU acceleration
- JIT-specialized execution
- Domain-specific wheels
- Commercial or enterprise licensing/support features

No higher-tier runtime is implemented by this repository.

## Installation

### From source

The repository is the authoritative installation path for the current remediation state:

```bash
git clone https://github.com/ficklecreationstudios-boop/crystalline-tier1.git
cd crystalline-tier1
pip install -e .
```

A PyPI installation command is intentionally not advertised here because a public PyPI release was not verified during this audit.

## System requirements

- Python 3.10 or higher
- NumPy >= 1.19.0
- SciPy >= 1.5.0
- Windows, macOS, or Linux

## Quick start

```python
import numpy as np
from crystalline import get_backend

backend = get_backend()
data = np.random.default_rng(0).normal(size=1024)

freqs, psd = backend.spectral_analysis(data, fs=100.0)
print(freqs.shape, psd.shape)
```

`spectral_analysis` uses a direct real FFT and density normalization consistent with SciPy's periodogram convention (`detrend=False`, `scaling="density"`).

## Documentation

- [Usage Guide](./docs/tier1-guide.md)
- [API Reference](./docs/api-reference.md)
- [Troubleshooting](./docs/troubleshooting.md)

## Validation

The repository contains independent numerical tests under `tests/`. These compare core results against established NumPy/SciPy reference behavior rather than benchmarking the implementation against itself.

Performance claims should be treated as benchmark-specific. Historical benchmark artifacts in `benchmarks/` are retained for auditability and are not a basis for a blanket speed-up claim. The current CI workflow also runs a reproducible benchmark only after the cross-platform correctness matrix passes; its results are evidence for the tested environment and workloads only.

## Licensing

This Tier 1 edition is released under the **GPL-3.0 License**. See [LICENSE](./LICENSE).

## Support and contributions

Please use [GitHub Issues](https://github.com/ficklecreationstudios-boop/crystalline-tier1/issues) for bug reports and project discussion. Contributions are welcome; see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Roadmap

- [x] Core spectral analysis
- [x] CPU-based linear algebra
- [x] Independent numerical correctness checks
- [x] Reproducible benchmark suite and methodology
- [x] Expanded usage examples
- [x] Broader numerical test coverage

## Disclaimer

This software is provided AS-IS under the GPL-3.0 License. It is a CPU-only research and experimentation library. No claim of universal acceleration, GPU execution, or production suitability is made by this Tier 1 repository.
