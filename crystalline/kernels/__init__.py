"""
crystalline/kernels/__init__.py
Tier 1 Kernels (CPU-based implementations)

This module provides CPU-only kernel implementations suitable for Tier 1.
GPU kernels are not available in this free edition.
"""

# Re-export from backend for convenience
from crystalline.backend import CPUBackend

# Tier 1 available kernels
AVAILABLE_KERNELS_TIER1 = [
    "spectral_analysis",
    "spectral_filtering",
    "convolution",
    "correlation",
    "fft",
    "ifft",
    "matrix_multiply",
    "matrix_solve",
    "qr_decomposition",
    "svd_decomposition",
]

# Higher tier kernels (NOT AVAILABLE)
UNAVAILABLE_KERNELS_HIGHER_TIERS = {
    "gpu_spectral_analysis": "Tier 2+",
    "gpu_convolution": "Tier 2+",
    "champion_mode": "Tier 4",
    "jit_specialization": "Tier 4",
    "domain_kernels": "Tier 3+",
}

def list_available_kernels():
    """List all available kernels in Tier 1."""
    return AVAILABLE_KERNELS_TIER1

def list_unavailable_kernels():
    """List kernels available in higher tiers only."""
    return UNAVAILABLE_KERNELS_HIGHER_TIERS

__all__ = [
    "AVAILABLE_KERNELS_TIER1",
    "UNAVAILABLE_KERNELS_HIGHER_TIERS",
    "list_available_kernels",
    "list_unavailable_kernels",
]
