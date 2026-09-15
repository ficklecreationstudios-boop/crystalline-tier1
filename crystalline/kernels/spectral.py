"""Experimental CPU spectral helpers for Tier 1.

These helpers are retained as source-visible utilities. They are not the public
backend path, and this module intentionally makes no performance claim until a
reproducible benchmark has been established.
"""

import numpy as np
from scipy import signal
from typing import Tuple, Optional

try:
    from numba import njit
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False

    def njit(func):
        return func


class WindowCache:
    """Cache window functions to avoid repeated construction."""

    def __init__(self, max_size: int = 128):
        self.max_size = max_size
        self._cache = {}

    def get(self, window: str, length: int) -> np.ndarray:
        """Get or create a window function."""
        key = (window, length)
        if key not in self._cache:
            if len(self._cache) >= self.max_size:
                self._cache.pop(next(iter(self._cache)))
            self._cache[key] = signal.get_window(window, length)
        return self._cache[key]

    def clear(self):
        """Clear all cached windows."""
        self._cache.clear()


_window_cache = WindowCache()


if HAS_NUMBA:
    @njit
    def _hamming_window(N: int) -> np.ndarray:
        result = np.zeros(N, dtype=np.float64)
        if N == 1:
            result[0] = 1.0
            return result
        for i in range(N):
            result[i] = 0.54 - 0.46 * np.cos(2.0 * np.pi * i / (N - 1))
        return result

    @njit
    def _hann_window(N: int) -> np.ndarray:
        result = np.zeros(N, dtype=np.float64)
        if N == 1:
            result[0] = 1.0
            return result
        for i in range(N):
            result[i] = 0.5 - 0.5 * np.cos(2.0 * np.pi * i / (N - 1))
        return result

    @njit
    def _blackman_window(N: int) -> np.ndarray:
        result = np.zeros(N, dtype=np.float64)
        if N == 1:
            result[0] = 1.0
            return result
        for i in range(N):
            result[i] = (
                0.42
                - 0.5 * np.cos(2.0 * np.pi * i / (N - 1))
                + 0.08 * np.cos(4.0 * np.pi * i / (N - 1))
            )
        return result

    @njit
    def _apply_window_jit(data: np.ndarray, window: np.ndarray) -> np.ndarray:
        return data * window

    def _get_window_numba(window_name: str, N: int) -> Optional[np.ndarray]:
        if window_name == "hamming":
            return _hamming_window(N)
        if window_name == "hann":
            return _hann_window(N)
        if window_name == "blackman":
            return _blackman_window(N)
        return None

else:
    def _get_window_numba(window_name: str, N: int) -> None:
        return None


def spectral_analysis(
    data: np.ndarray,
    fs: float = 1.0,
    window: str = "hamming",
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute one-sided density-scaled PSD using the Tier 1 convention."""
    data = np.asarray(data, dtype=np.float64)
    if fs <= 0:
        raise ValueError("fs must be positive")
    if data.ndim != 1:
        raise ValueError("spectral_analysis expects a one-dimensional signal")
    if data.size == 0:
        raise ValueError("spectral_analysis requires at least one sample")

    N = data.size
    window_func = _window_cache.get(window, N)
    windowed_data = data * window_func
    fft_result = np.fft.rfft(windowed_data)
    psd = (np.abs(fft_result) ** 2) / (fs * np.sum(window_func**2))

    if N > 1:
        if N % 2 == 0:
            psd[1:-1] *= 2.0
        else:
            psd[1:] *= 2.0

    freqs = np.fft.rfftfreq(N, d=1.0 / fs)
    return freqs, psd


def rfft(data: np.ndarray, fs: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
    """Compute a real FFT and its frequency coordinates."""
    data = np.asarray(data, dtype=np.float64)
    if fs <= 0:
        raise ValueError("fs must be positive")
    if data.ndim != 1:
        raise ValueError("rfft expects a one-dimensional signal")
    if data.size == 0:
        raise ValueError("rfft requires at least one sample")
    fft_result = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(data.size, 1.0 / fs)
    return freqs, fft_result


def irfft(fft_data: np.ndarray, N: Optional[int] = None) -> np.ndarray:
    """Compute the inverse real FFT."""
    return np.fft.irfft(fft_data, N)


def periodogram(
    data: np.ndarray,
    fs: float = 1.0,
    window: str = "hamming",
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute a Welch PSD using SciPy's ``signal.welch`` convention."""
    if fs <= 0:
        raise ValueError("fs must be positive")
    return signal.welch(data, fs=fs, window=window)


def stft(
    data: np.ndarray,
    fs: float = 1.0,
    window: str = "hann",
    nperseg: int = 256,
    noverlap: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute a short-time Fourier transform using SciPy."""
    if fs <= 0:
        raise ValueError("fs must be positive")
    if nperseg <= 0:
        raise ValueError("nperseg must be positive")
    if noverlap is not None and not 0 <= noverlap < nperseg:
        raise ValueError("noverlap must satisfy 0 <= noverlap < nperseg")
    if noverlap is None:
        noverlap = nperseg // 2
    freqs, times, Sxx = signal.stft(
        data, fs=fs, window=window, nperseg=nperseg, noverlap=noverlap
    )
    return times, freqs, Sxx


__all__ = [
    "spectral_analysis",
    "rfft",
    "irfft",
    "periodogram",
    "stft",
    "WindowCache",
]
