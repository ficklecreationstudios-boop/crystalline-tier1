"""Crystalline Tier 1 — free, CPU-only edition."""

__version__ = "5.0.1-tier1"
__tier__ = "TIER_1_FREE"
__author__ = "Crystalline Project Contributors"
__license__ = "GPL-3.0"

import os

# Tier 1 enforcement: this distribution is CPU-only.
os.environ["CRYSTALLINE_TIER"] = "TIER_1_FREE"
os.environ["CRYSTALLINE_SKIP_LICENSE_VALIDATION"] = "1"

from crystalline.licensing import check_tier_access
from crystalline.api import spectral_analysis, spectral_filtering


def get_backend():
    """Get the Tier 1 CPU backend."""
    from crystalline.backend import get_backend as _get_backend

    return _get_backend()


def get_tier_info():
    """Return the capabilities exposed by this distribution."""
    return {
        "tier": "TIER_1_FREE",
        "version": __version__,
        "gpu_available": False,
        "champion_mode_available": False,
        "jit_available": False,
        "description": "Free, open-source CPU-only edition",
    }


# Validate that the installed tier can use the core Tier 1 API.
check_tier_access("spectral_analysis")

__all__ = [
    "get_backend",
    "spectral_analysis",
    "spectral_filtering",
    "get_tier_info",
    "__version__",
    "__tier__",
]
