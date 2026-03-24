# Crystalline GPU - Tier 1 (Free Edition)

![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)
![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen)
![Platform: Cross-platform](https://img.shields.io/badge/Platform-Cross--platform-lightgrey)

**Open-source, CPU-based GPU acceleration library for learning and experimentation.**

## ⚠️ Tier 1 (Free) - CPU Only

This is the **free, open-source Tier 1 edition** of Crystalline GPU. It provides:

✅ **Available Features:**
- Core spectral analysis algorithms (CPU-based)
- Linear algebra operations (NumPy/SciPy-backed)
- Signal processing utilities
- Educational and research use
- Full source code transparency

❌ **NOT Available (Higher Tiers Only):**
- GPU acceleration (requires Tier 2+)
- Champion Mode optimization (Tier 4 only)
- JIT specialization (Tier 4 only)
- Domain-specific wheels (Tier 3+)
- Commercial licensing (Tier 2+)
- Hardware-bound licensing (Tier 2+)
- Enterprise support (Tier 3+)

## Installation

### From PyPI (recommended)

```bash
pip install crystalline-tier1
```

### From source

```bash
git clone https://github.com/yourusername/crystalline-tier1.git
cd crystalline-tier1
pip install -e .
```

### System Requirements

- Python 3.10 or higher
- NumPy >= 1.19.0
- SciPy >= 1.5.0
- Cross-platform (Windows, macOS, Linux)

## Quick Start

```python
from crystalline import get_backend

# Get the Tier 1 (CPU) backend
backend = get_backend()

# Use available tier 1 operations
import numpy as np
data = np.random.randn(1024)

# Spectral analysis (CPU-based)
result = backend.spectral_analysis(data)
print(result)
```

## Documentation

- **[Usage Guide](./docs/tier1-guide.md)** - Detailed examples and API reference
- **[API Reference](./docs/api-reference.md)** - Complete API documentation
- **[Troubleshooting](./docs/troubleshooting.md)** - Common issues and solutions

## Licensing

This Tier 1 edition is released under the **GPL-3.0 License** for open-source use.

See [LICENSE](./LICENSE) for details.

### For Higher Tiers:

- **Tier 2** (GPU) - Commercial: Contact [SALES_EMAIL]
- **Tier 3** (Domain Wheels) - Enterprise: Contact [SALES_EMAIL]  
- **Tier 4** (Champion Mode) - Premium: Contact [SALES_EMAIL]

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/crystalline-tier1/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/crystalline-tier1/discussions)
- **Commercial Support**: [CONTACT_EMAIL]

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## Roadmap

- [x] Core spectral analysis (Tier 1)
- [x] CPU-based linear algebra
- [ ] Performance documentation
- [ ] Usage examples database
- [ ] Community contributions

## Disclaimer

This Tier 1 edition is provided AS-IS for educational and research purposes. For production GPU-accelerated workloads, see [Tier 2+ licensing](TIER2_INFO).

---

**Crystalline GPU**: Universally accelerated computing.
