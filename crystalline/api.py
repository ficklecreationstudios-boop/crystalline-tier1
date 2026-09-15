"""
Public API for Tier 1 (CPU-only operations).
"""

from crystalline.backend import get_backend
from crystalline.licensing import check_tier_access


def spectral_analysis(data, fs=None, window="hamming"):
    """Perform one-sided power spectral density analysis on input data.

    Args:
        data: One-dimensional input signal.
        fs: Sampling frequency (default: 1.0).
        window: Window accepted by ``scipy.signal.get_window``.

    Returns:
        Tuple of (frequencies, power_spectral_density).
    """
    check_tier_access("spectral_analysis")
    return get_backend().spectral_analysis(data, fs=fs, window=window)


def spectral_filtering(data, cutoff, order=4, btype="low"):
    """Apply a digital Butterworth filter.

    ``cutoff`` uses SciPy's normalized digital-filter convention because the
    public Tier 1 API does not expose a sampling-frequency argument: scalar
    values and band edges must therefore lie strictly between 0 and 1, where
    1 is the Nyquist frequency.
    """
    check_tier_access("spectral_filtering")
    return get_backend().spectral_filtering(data, cutoff, order=order, btype=btype)


__all__ = ["get_backend", "spectral_analysis", "spectral_filtering"]
