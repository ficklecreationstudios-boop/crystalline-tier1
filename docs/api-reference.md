# Crystalline GPU - Tier 1 API Reference

## Module: `crystalline`

### Functions

#### `get_backend()`

Returns the Tier 1 CPU backend instance.

**Returns:**
- `CPUBackend`: CPU computation backend

**Example:**
```python
from crystalline import get_backend
backend = get_backend()
```

#### `spectral_analysis(data, fs=None, window='hamming')`

Perform spectral analysis using FFT.

**Parameters:**
- `data` (array-like): Input signal
- `fs` (float, optional): Sampling frequency. Default: 1.0
- `window` (str, optional): Window function. Default: 'hamming'
  - Options: 'hamming', 'hann', 'blackman', 'bartlett', 'kaiser'

**Returns:**
- `tuple`: (frequencies, power_spectral_density)
  - frequencies: Array of frequency values
  - psd: Array of power values

**Raises:**
- `TierFeatureBlockedError`: If called from non-Tier-1

**Example:**
```python
import numpy as np
from crystalline import spectral_analysis

signal = np.random.randn(1024)
freqs, psd = spectral_analysis(signal, fs=100.0, window='hann')
```

#### `spectral_filtering(data, cutoff, order=4, btype='low')`

Apply frequency-domain digital filter.

**Parameters:**
- `data` (array-like): Input signal
- `cutoff` (float or float array): Cutoff frequency/frequencies
- `order` (int, optional): Filter order. Default: 4
- `btype` (str, optional): Filter type. Default: 'low'
  - Options: 'low', 'high', 'band', 'bandstop'

**Returns:**
- `ndarray`: Filtered signal

**Raises:**
- `TierFeatureBlockedError`: If called from non-Tier-1

**Example:**
```python
from crystalline import spectral_filtering

# Low-pass filter
filtered = spectral_filtering(signal, cutoff=50, order=5, btype='low')

# Band-pass filter
filtered = spectral_filtering(signal, cutoff=[20, 80], btype='band')
```

### Classes

#### `CPUBackend`

CPU computation backend for Tier 1.

**Attributes:**
- `device`: String "cpu"
- `gpu_available`: Boolean False
- `tier`: String "TIER_1_FREE"

**Methods:**

##### `spectral_analysis(data, fs=None, window='hamming')`
Alias for module-level `spectral_analysis()`.

##### `spectral_filtering(data, cutoff, order=4, btype='low')`
Alias for module-level `spectral_filtering()`.

##### `convolution(input_data, kernel, padding=0, stride=1, **kwargs)`
Perform convolution on input with kernel.

**Parameters:**
- `input_data`: Input array
- `kernel`: Convolution kernel
- `padding`: Padding amount (default: 0)
- `stride`: Stride amount (default: 1)

**Returns:**
- Convolved result

##### `linear_algebra_solve(A, b)`
Solve linear system Ax=b.

**Parameters:**
- `A`: Coefficient matrix (n, n)
- `b`: Right-hand side (n,)

**Returns:**
- Solution vector (n,)

##### `matrix_multiply(A, B)`
Perform matrix multiplication.

**Parameters:**
- `A`: First matrix
- `B`: Second matrix

**Returns:**
- Product matrix

## Module: `crystalline.licensing`

### Functions

#### `get_tier()`
Returns current tier. Always "TIER_1_FREE" in this distribution.

**Returns:**
- `str`: "TIER_1_FREE"

#### `check_tier_access(feature_name)`
Check if feature is available in current tier.

**Parameters:**
- `feature_name` (str): Feature to check

**Returns:**
- `bool`: True if available

**Raises:**
- `TierFeatureBlockedError`: If feature not available

**Example:**
```python
from crystalline.licensing import check_tier_access

check_tier_access("spectral_analysis")  # Returns True
check_tier_access("gpu_acceleration")   # Raises TierFeatureBlockedError
```

#### `is_tier_1_only()`
Check if running in Tier 1 only mode.

**Returns:**
- `bool`: True if Tier 1

#### `get_license_info()`
Get license information.

**Returns:**
- `dict`: License info including tier, source (GPL-3.0), etc.

### Classes

#### `TierFeatureBlockedError`
Raised when accessing non-Tier-1 features.

**Inherits from:**
- `Tier1EnforcementError`
- `Exception`

## Module: `crystalline.kernels`

### Functions

#### `list_available_kernels()`
List all available kernels in Tier 1.

**Returns:**
- `list`: List of kernel names

**Example:**
```python
from crystalline.kernels import list_available_kernels
kernels = list_available_kernels()
print(kernels)
# ['spectral_analysis', 'spectral_filtering', 'convolution', ...]
```

#### `list_unavailable_kernels()`
List kernels available only in higher tiers.

**Returns:**
- `dict`: Mapping of kernel names to required tier

**Example:**
```python
from crystalline.kernels import list_unavailable_kernels
higher_tier = list_unavailable_kernels()
print(higher_tier)
# {'gpu_spectral_analysis': 'Tier 2+', 'champion_mode': 'Tier 4', ...}
```

## Error Handling

### Common Errors

#### `TierFeatureBlockedError`
Raised when attempting to use a higher-tier feature.

```python
from crystalline.backend import GPUBackend

try:
    gpu = GPUBackend()  # Tier 1 doesn't have GPU
except TierFeatureBlockedError as e:
    print(f"Error: {e}")
    print("Please upgrade to Tier 2+ for GPU support")
```

#### `ImportError`
Raised if dependencies (NumPy, SciPy) are missing.

```bash
pip install numpy scipy
```

## Tier System

### Tier Availability Matrix

| Feature | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---------|--------|--------|--------|--------|
| Spectral Analysis | ✅ | ✅ | ✅ | ✅ |
| Signal Processing | ✅ | ✅ | ✅ | ✅ |
| Linear Algebra (CPU) | ✅ | ✅ | ✅ | ✅ |
| GPU Acceleration | ❌ | ✅ | ✅ | ✅ |
| Champion Mode | ❌ | ❌ | ❌ | ✅ |
| JIT Specialization | ❌ | ❌ | ❌ | ✅ |
| Domain Wheels | ❌ | ❌ | ✅ | ✅ |

### Upgrading Tiers

To access higher-tier features:

1. Visit https://crystalline.io/tiers
2. Contact [SALES_EMAIL]
3. Reference the tier feature matrix above

## License

This Tier 1 edition is released under GPL-3.0. See LICENSE file for details.
