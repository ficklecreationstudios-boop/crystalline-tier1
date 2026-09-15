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
        """Compute a one-sided, density-scaled power spectral density."""
        check_tier_access("spectral_analysis")
        data = np.asarray(data, dtype=np.float64)
        fs = 1.0 if fs is None else fs
        if fs <= 0:
            raise ValueError("fs must be positive")
        if data.ndim != 1:
            raise ValueError("spectral_analysis expects a one-dimensional signal")
        if data.size == 0:
            raise ValueError("spectral_analysis requires at least one sample")
        window_func = signal.get_window(window, data.size)
        fft_result = np.fft.rfft(data * window_func)
        psd = (np.abs(fft_result) ** 2) / (fs * np.sum(window_func**2))
        if data.size > 1:
            if data.size % 2 == 0:
                psd[1:-1] *= 2.0
            else:
                psd[1:] *= 2.0
        freqs = np.fft.rfftfreq(data.size, d=1.0 / fs)
        return freqs, psd

    def spectral_filtering(self, data, cutoff, order=4, btype="low"):
        """Apply a one-dimensional Butterworth digital filter with normalized cutoffs."""
        check_tier_access("spectral_filtering")
        data = np.asarray(data, dtype=np.float64)
        if data.ndim != 1:
            raise ValueError("spectral_filtering expects a one-dimensional signal")
        if data.size == 0:
            raise ValueError("spectral_filtering requires at least one sample")
        if not isinstance(order, (int, np.integer)) or order <= 0:
            raise ValueError("order must be a positive integer")
        try:
            b, a = signal.butter(order, cutoff, btype=btype)
            return signal.filtfilt(b, a, data)
        except ValueError as exc:
            raise ValueError(f"invalid filter parameters or input: {exc}") from exc

    def convolution(self, input_data, kernel, padding=0, stride=1, **kwargs):
        """Perform one-dimensional same-mode convolution on the CPU."""
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
        return signal.convolve(input_data, kernel, mode="same")[::stride]

    def linear_algebra_solve(self, A, b):
        """Solve a square linear system Ax=b on the CPU."""
        check_tier_access("linear_algebra")
        A = np.asarray(A, dtype=np.float64)
        b = np.asarray(b, dtype=np.float64)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("A must be a two-dimensional square matrix")
        if b.ndim not in (1, 2) or b.shape[0] != A.shape[0]:
            raise ValueError("b must have one or two dimensions with a matching row count")
        try:
            return linalg.solve(A, b)
        except (ValueError, linalg.LinAlgError) as exc:
            raise ValueError(f"linear system could not be solved: {exc}") from exc

    def matrix_multiply(self, A, B):
        """Perform two-dimensional matrix multiplication on the CPU."""
        check_tier_access("linear_algebra")
        A = np.asarray(A)
        B = np.asarray(B)
        if A.ndim != 2 or B.ndim != 2:
            raise ValueError("matrix_multiply expects two-dimensional matrices")
        if A.shape[1] != B.shape[0]:
            raise ValueError("matrix dimensions are incompatible for multiplication")
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


__all__ = ["CPUBackend", "GPUBackend", "get_backend", "set_backend"]
