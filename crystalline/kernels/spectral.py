"""Experimental CPU spectral helpers for Tier 1.

These helpers are retained as source-visible utilities. They are not the public
backend path, and this module intentionally makes no performance claim until a
reproducible benchmark has been established.
"""

import numpy as np
from scipy import signal
from typing import Tuple, Optional


class WindowCache:
    """Cache SciPy-compatible window functions to avoid repeated construction."""

    def __init__(self, max_size: int = 128):
        if not isinstance(max_size, int) or max_size <= 0:
            raise ValueError("max_size must be a positive integer")
        self.max_size = max_size
        self._cache = {}

    def get(self, window: str, length: int) -> np.ndarray:
        """Get or create a SciPy-compatible window function."""
        if not isinstance(length, int) or length <= 0:
            raise ValueError("length must be a positive integer")
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
    """Compute a one-sided density-scaled periodogram.

    The implementation delegates to SciPy's ``signal.periodogram`` with
    detrending disabled so its semantics match ``spectral_analysis``.
    """
    data = np.asarray(data, dtype=np.float64)
    if fs <= 0:
        raise ValueError("fs must be positive")
    if data.ndim != 1:
        raise ValueError("periodogram expects a one-dimensional signal")
    if data.size == 0:
        raise ValueError("periodogram requires at least one sample")

    return signal.periodogram(
        data,
        fs=fs,
        window=window,
        detrend=False,
        scaling="density",
        return_onesided=True,
    )


def stft(
    data: np.ndarray,
    fs: float = 1.0,
    window: str = "hann",
    nperseg: int = 256,
    noverlap: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute an STFT and return ``(times, frequencies, coefficients)``.

    This helper intentionally uses a different return order from SciPy's
    ``signal.stft`` (which returns ``(frequencies, times, coefficients)``).
    The ordering is part of this helper's explicit contract.
    """
    data = np.asarray(data, dtype=np.float64)
    if data.ndim != 1:
        raise ValueError("stft expects a one-dimensional signal")
    if data.size == 0:
        raise ValueError("stft requires at least one sample")
    if fs <= 0:
        raise ValueError("fs must be positive")
    if not isinstance(nperseg, (int, np.integer)) or nperseg <= 0:
        raise ValueError("nperseg must be a positive integer")
    if noverlap is not None and not isinstance(noverlap, (int, np.integer)):
        raise ValueError("noverlap must be an integer or None")
    if noverlap is not None and not 0 <= noverlap < nperseg:
        raise ValueError("noverlap must satisfy 0 <= noverlap < nperseg")
    if noverlap is None:
        noverlap = nperseg // 2
    freqs, times, coefficients = signal.stft(
        data, fs=fs, window=window, nperseg=nperseg, noverlap=noverlap
    )
    return times, freqs, coefficients


__all__ = [
    "spectral_analysis",
    "rfft",
    "irfft",
    "periodogram",
    "stft",
    "WindowCache",
]
