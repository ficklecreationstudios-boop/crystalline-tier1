"""CPU kernel inventory for the published Tier 1 distribution.

The inventory names operations that are actually implemented by
:class:`crystalline.backend.CPUBackend`. It is an availability description,
not a promise of higher-tier products or performance.
"""

from crystalline.backend import CPUBackend

# Keep this list aligned with concrete CPUBackend methods. Public wrappers
# may expose only a subset of these operations.
AVAILABLE_KERNELS_TIER1 = [
    "spectral_analysis",
    "spectral_filtering",
    "convolution",
    "linear_algebra_solve",
    "matrix_multiply",
]

# Features intentionally not implemented by this repository. The values are
# factual availability reasons, not commercial tier/pricing promises.
UNAVAILABLE_KERNELS_HIGHER_TIERS = {
    "gpu_spectral_analysis": "not implemented in Tier 1",
    "gpu_convolution": "not implemented in Tier 1",
    "champion_mode": "not implemented",
    "jit_specialization": "not implemented",
    "domain_kernels": "not implemented",
}


def list_available_kernels():
    """Return a copy of the implemented Tier 1 kernel names."""
    return list(AVAILABLE_KERNELS_TIER1)


def list_unavailable_kernels():
    """Return a copy of the unavailable feature inventory."""
    return dict(UNAVAILABLE_KERNELS_HIGHER_TIERS)


__all__ = [
    "CPUBackend",
    "AVAILABLE_KERNELS_TIER1",
    "UNAVAILABLE_KERNELS_HIGHER_TIERS",
    "list_available_kernels",
    "list_unavailable_kernels",
]
