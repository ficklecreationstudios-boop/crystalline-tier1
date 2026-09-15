"""
crystalline/backend.py
Backend management for Tier 1 (CPU only).
"""

import numpy as np
from scipy import linalg, signal
from crystalline.licensing import TierFeatureBlockedError, check_tier_access


class CPUBackend:
    """CPU-only backend for Tier 1."""

    def __init__(self):
        self.device = "cpu"
        self.gpu_available = False
        self.tier = "TIER_1_FREE"

    def spectral_analysis(self, data, fs=None, window="hamming"):
        """Compute a one-sided, density-scaled power spectral density.

        The result follows the numerical convention of
        ``scipy.signal.periodogram(..., detrend=False, scaling='density')``.
        """
        check_tier_access("spectral_analysis")

        data = np.asarray(data, dtype=np.float64)
        if fs is None:
            fs = 1.0
        if fs <= 0:
            raise ValueError("fs must be positive")
        if data.ndim != 1:
            raise ValueError("spectral_analysis expects a one-dimensional signal")
        if data.size == 0:
            raise ValueError("spectral_analysis requires at least one sample")

        n_samples = data.size
        window_func = signal.get_window(window, n_samples)
        windowed_data = data * window_func

        fft_result = np.fft.rfft(windowed_data)
        window_power = np.sum(window_func**2)
        psd = (np.abs(fft_result) ** 2) / (fs * window_power)

        # Double positive-frequency bins, excluding DC and (for even N)
        # Nyquist. For odd N, the final bin is not a Nyquist bin.
        if n_samples > 1:
            if n_samples % 2 == 0:
                psd[1:-1] *= 2.0
            else:
                psd[1:] *= 2.0

        freqs = np.fft.rfftfreq(n_samples, d=1.0 / fs)
        return freqs, psd

    def spectral_filtering(self, data, cutoff, order=4, btype="low"):
        """Apply a one-dimensional Butterworth digital filter.

        ``cutoff`` follows SciPy's normalized digital-filter convention:
        scalar cutoffs and band edges must lie strictly between 0 and 1,
        where 1 is the Nyquist frequency. The public Tier 1 filtering API
        accepts one-dimensional signals only.
        """
        check_tier_access("spectral_filtering")
        data = np.asarray(data, dtype=np.float64)
        if data.ndim != 1:
            raise ValueError("spectral_filtering expects a one-dimensional signal")
        if data.size == 0:
            raise ValueError("spectral_filtering requires at least one sample")
        if not isinstance(order, (int, np.integer)) or order <= 0:
            raise ValueError("order must be a positive integer")

        b, a = signal.butter(order, cutoff, btype=btype)
        try:
            return signal.filtfilt(b, a, data)
        except ValueError as exc:
            raise ValueError(
                "input signal is too short for the requested Butterworth filter"
            ) from exc

    def convolution(self, input_data, kernel, padding=0, stride=1, **kwargs):
        """Perform one-dimensional convolution on the CPU.

        ``mode='same'`` is retained for compatibility with the original Tier 1
        API. Padding is applied before convolution, and stride selects every
        ``stride``-th result from the same-mode output.
        """
        check_tier_access("convolution")

        if not isinstance(stride, (int, np.integer)) or stride <= 0:
            raise ValueError("stride must be a positive integer")
        if not isinstance(padding, (int, np.integer)) or padding < 0:
            raise ValueError("padding must be a non-negative integer")

        input_data = np.asarray(input_data)
        kernel = np.asarray(kernel)
        if input_data.ndim != 1:
            raise ValueError("convolution expects one-dimensional input_data")
        if kernel.ndim != 1:
            raise ValueError("convolution expects a one-dimensional kernel")
        if input_data.size == 0 or kernel.size == 0:
            raise ValueError("convolution requires non-empty input_data and kernel")

        if padding > 0:
            input_data = np.pad(input_data, padding, mode="constant")

        result = signal.convolve(input_data, kernel, mode="same")
        return result[::stride]

    def linear_algebra_solve(self, A, b):
        """Solve linear system Ax=b (CPU)."""
        check_tier_access("linear_algebra")
        A = np.asarray(A, dtype=np.float64)
        b = np.asarray(b, dtype=np.float64)
        return linalg.solve(A, b)

    def matrix_multiply(self, A, B):
        """Perform matrix multiplication (CPU)."""
        check_tier_access("linear_algebra")
        return np.matmul(A, B)


class GPUBackend:
    """Placeholder for a future GPU backend; unavailable in Tier 1."""

    def __init__(self):
        raise TierFeatureBlockedError(
            "GPU acceleration is not implemented in this CPU-only Tier 1 distribution."
        )


_backend = None


def get_backend():
    """Get the Tier 1 CPU backend."""
    global _backend
    if _backend is None:
        _backend = CPUBackend()
    return _backend


def set_backend(backend_type="cpu"):
    """Set the backend type; only the CPU backend is implemented."""
    if backend_type != "cpu":
        raise TierFeatureBlockedError(
            f"Backend '{backend_type}' is not implemented in this CPU-only Tier 1 distribution."
        )

    global _backend
    _backend = CPUBackend()
    return _backend


__all__ = [
    "CPUBackend",
    "GPUBackend",
    "get_backend",
    "set_backend",
]
