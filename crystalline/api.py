"""
crystalline/api.py
Public API for Tier 1 (CPU-only operations)

This module provides the primary access point for Tier 1 features.
"""

import numpy as np
from crystalline.backend import get_backend
from crystalline.licensing import check_tier_access

def get_backend():
    """Get the Tier 1 CPU backend.
    
    Returns:
        CPU backend instance for spectral analysis and linear algebra
    """
    from crystalline.backend import get_backend as _get_backend
    return _get_backend()

def spectral_analysis(data, fs=None, window='hamming'):
    """Perform spectral analysis on input data.
    
    Computes the power spectral density using FFT (CPU-based).
    
    Args:
        data: Input signal (numpy array)
        fs: Sampling frequency (default: 1.0)
        window: Window function ('hamming', 'hann', 'blackman', etc.)
        
    Returns:
        Tuple of (frequencies, power_spectral_density)
        
    Raises:
        TierFeatureBlockedError: If accessed from non-Tier 1
        
    Example:
        >>> import numpy as np
        >>> from crystalline import spectral_analysis
        >>> data = np.random.randn(1024)
        >>> freqs, psd = spectral_analysis(data, fs=100.0)
    """
    check_tier_access("spectral_analysis")
    
    backend = get_backend()
    return backend.spectral_analysis(data, fs=fs, window=window)

def spectral_filtering(data, cutoff, order=4, btype='low'):
    """Apply digital filter in frequency domain.
    
    Args:
        data: Input signal
        cutoff: Cutoff frequency (or frequencies for bandpass)
        order: Filter order (default: 4)
        btype: Filter type ('low', 'high', 'band', 'bandstop')
        
    Returns:
        Filtered signal
        
    Raises:
        TierFeatureBlockedError: If accessed from non-Tier 1
        
    Example:
        >>> from crystalline import spectral_filtering
        >>> filtered = spectral_filtering(data, cutoff=10, btype='low')
    """
    check_tier_access("spectral_filtering")
    
    backend = get_backend()
    return backend.spectral_filtering(data, cutoff, order=order, btype=btype)

__all__ = [
    "get_backend",
    "spectral_analysis",
    "spectral_filtering",
]
