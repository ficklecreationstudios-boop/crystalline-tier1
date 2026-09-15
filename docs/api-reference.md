# Crystalline Tier 1 API Reference

## Module: `crystalline`

### `get_backend()`

Returns the Tier 1 CPU backend instance.

### `spectral_analysis(data, fs=None, window='hamming')`

Computes a one-sided, density-scaled power spectral density using a real FFT. The numerical convention matches `scipy.signal.periodogram(..., detrend=False, scaling='density')` for the supported windowed input.

**Parameters**
- `data`: one-dimensional input signal; empty or multi-dimensional input is rejected
- `fs`: positive sampling frequency; defaults to `1.0`
- `window`: any window accepted by `scipy.signal.get_window`; defaults to `hamming`

**Returns**
- `(frequencies, psd)`: frequency bins and PSD values

### `spectral_filtering(data, cutoff, order=4, btype='low')`

Applies a one-dimensional Butterworth digital filter through SciPy's `butter`/`filtfilt` implementation.

**Parameters**
- `data`: one-dimensional, non-empty input signal
- `cutoff`: scalar cutoff or band edges accepted by SciPy's `butter`
- `order`: positive integer filter order
- `btype`: filter type accepted by SciPy's `butter`

**Cutoff convention:** because this API does not accept `fs`, cutoff values use SciPy's normalized digital-filter convention: scalar cutoffs and band edges must be strictly between `0` and `1`, with `1` representing Nyquist.

Signals that are too short for the requested filter are rejected with `ValueError` rather than exposing SciPy's lower-level padding error.

Example:
```python
filtered = spectral_filtering(signal, cutoff=0.2, order=5, btype='low')
filtered = spectral_filtering(signal, cutoff=[0.1, 0.4], btype='band')
```

### `CPUBackend`

CPU-only Tier 1 backend.

Attributes:
- `device == "cpu"`
- `gpu_available == False`
- `tier == "TIER_1_FREE"`

Methods include `spectral_analysis`, `spectral_filtering`, `convolution`, `linear_algebra_solve`, and `matrix_multiply`.

#### `convolution(input_data, kernel, padding=0, stride=1)`

Performs one-dimensional convolution using SciPy's `signal.convolve(..., mode='same')`. Both `input_data` and `kernel` must be non-empty one-dimensional arrays. Optional zero padding is applied before convolution. `stride` must be a positive integer and returns every `stride`-th value of the resulting same-mode output.

#### `linear_algebra_solve(A, b)`

Solves `Ax=b` using SciPy linear algebra routines.

#### `matrix_multiply(A, B)`

Performs matrix multiplication using NumPy's `matmul`.

## Module: `crystalline.licensing`

Tier 1 exposes the CPU features in this repository. GPU and higher-tier features are intentionally unavailable in this distribution.

## Module: `crystalline.kernels`

`list_available_kernels()` returns the Tier 1 kernel names exposed by the package. `list_unavailable_kernels()` describes higher-tier features that are not implemented here.

## Experimental spectral helpers

`crystalline.kernels.spectral` contains source-visible experimental helpers that are not part of the public top-level API. They intentionally make no performance claim.

- `spectral_analysis`, `periodogram`: one-dimensional density-scaled PSD helpers aligned to the documented SciPy convention.
- `rfft` / `irfft`: real FFT helpers.
- `stft`: returns `(times, frequencies, coefficients)`. This ordering is intentionally different from SciPy's `(frequencies, times, coefficients)` and is covered by an independent test.
- `WindowCache`: caches SciPy-compatible windows.

## Error handling

`TierFeatureBlockedError` is raised when a higher-tier feature is requested from the Tier 1 distribution, including attempts to instantiate `GPUBackend` or select a non-CPU backend.

## Tier 1 scope

| Feature | Tier 1 |
|---|---:|
| Spectral analysis | Yes |
| Signal filtering | Yes |
| Linear algebra (CPU) | Yes |
| GPU acceleration | No |
| JIT specialization | No |
| Domain-specific wheels | No |
| Champion mode | No |

This repository does not publish pricing, sales contacts, or claims about higher-tier availability beyond this capability boundary.

## License

This Tier 1 edition is released under GPL-3.0. See `LICENSE`.