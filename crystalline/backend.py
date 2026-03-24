"""
crystalline/backend.py
Backend management for Tier 1 (CPU only)

This module manages the computation backend. In Tier 1, only CPU
operations are available.
"""

import numpy as np
from scipy import signal, fft, linalg
from crystalline.licensing import check_tier_access, TierFeatureBlockedError

class CPUBackend:
    """CPU-only backend for Tier 1."""
    
    def __init__(self):
        self.device = "cpu"
        self.gpu_available = False
        self.tier = "TIER_1_FREE"
    
    def spectral_analysis(self, data, fs=None, window='hamming'):
        """Perform spectral analysis using NumPy/SciPy (CPU).
        
        Args:
            data: Input signal
            fs: Sampling frequency (default: 1.0)
            window: Window function (default: 'hamming')
            
        Returns:
            Tuple of (frequencies, power_spectral_density)
        """
        check_tier_access("spectral_analysis")
        
        data = np.asarray(data)
        if fs is None:
            fs = 1.0
        
        # Compute FFT
        freqs, psd = signal.periodogram(data, fs=fs, window=window)
        return freqs, psd
    
    def spectral_filtering(self, data, cutoff, order=4, btype='low'):
        """Apply frequency domain filtering (CPU).
        
        Args:
            data: Input signal
            cutoff: Cutoff frequency
            order: Filter order (default: 4)
            btype: Filter type ('low', 'high', 'band', 'bandstop')
            
        Returns:
            Filtered signal
        """
        check_tier_access("spectral_filtering")
        
        data = np.asarray(data)
        
        # Design Butterworth filter
        b, a = signal.butter(order, cutoff, btype=btype)
        
        # Apply filter
        filtered = signal.filtfilt(b, a, data)
        return filtered
    
    def convolution(self, input_data, kernel, padding=0, stride=1, **kwargs):
        """Perform convolution (CPU).
        
        Args:
            input_data: Input tensor
            kernel: Convolution kernel
            padding: Padding amount
            stride: Stride amount
            
        Returns:
            Convolved result
        """
        check_tier_access("convolution")
        
        input_data = np.asarray(input_data)
        kernel = np.asarray(kernel)
        
        # Pad if necessary
        if padding > 0:
            input_data = np.pad(input_data, padding, mode='constant')
        
        # Simple 1D convolution for Tier 1
        return signal.convolve(input_data, kernel, mode='same')
    
    def linear_algebra_solve(self, A, b):
        """Solve linear system Ax=b (CPU).
        
        Args:
            A: Coefficient matrix
            b: Right-hand side
            
        Returns:
            Solution vector
        """
        check_tier_access("linear_algebra")
        
        A = np.asarray(A, dtype=np.float64)
        b = np.asarray(b, dtype=np.float64)
        
        return linalg.solve(A, b)
    
    def matrix_multiply(self, A, B):
        """Perform matrix multiplication (CPU).
        
        Args:
            A: First matrix
            B: Second matrix
            
        Returns:
            Product matrix
        """
        check_tier_access("linear_algebra")
        
        return np.matmul(A, B)

class GPUBackend:
    """GPU backend (NOT AVAILABLE IN TIER 1)."""
    
    def __init__(self):
        raise TierFeatureBlockedError(
            "GPU acceleration is not available in Tier 1 (free edition). "
            "For GPU support, please upgrade to Tier 2+. "
            "Visit https://[DOMAIN]/tiers for details or contact [SALES_EMAIL]"
        )

# Global backend instance
_backend = None

def get_backend():
    """Get the Tier 1 CPU backend.
    
    Note: GPU backends are not available in this tier 1 distribution.
    
    Returns:
        CPUBackend instance
    """
    global _backend
    if _backend is None:
        _backend = CPUBackend()
    return _backend

def set_backend(backend_type="cpu"):
    """Set backend type (CPU only in Tier 1).
    
    Args:
        backend_type: 'cpu' (only option for Tier 1)
        
    Raises:
        TierFeatureBlockedError: If trying to use GPU backend
    """
    if backend_type != "cpu":
        raise TierFeatureBlockedError(
            f"Backend '{backend_type}' is not available in Tier 1. "
            "Only CPU backend is available in this free edition. "
            "For GPU acceleration, upgrade to Tier 2+."
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
