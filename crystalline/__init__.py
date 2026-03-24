"""
crystalline/__init__.py
Crystalline GPU - Tier 1 (Free, CPU-only Edition)

Status: TIER 1 - CPU ONLY - OPEN SOURCE

This is the free tier of Crystalline GPU offering CPU-based implementations
for learning and research. GPU acceleration and advanced features require
commercial licensing (Tier 2+).

Tier Availability:
- Tier 1: FREE (this edition) - CPU only, open-source
- Tier 2: GPU acceleration ($500/month)
- Tier 3: Domain wheels ($100K+/year)
- Tier 4: Champion Mode ($300K+/year)
"""

__version__ = "5.0.0-tier1"
__tier__ = "TIER_1_FREE"
__author__ = "Crystalline Project Contributors"
__license__ = "GPL-3.0"

import os
import sys
import warnings

# TIER 1 ENFORCEMENT: Set the tier immediately
os.environ["CRYSTALLINE_TIER"] = "TIER_1_FREE"
os.environ["CRYSTALLINE_SKIP_LICENSE_VALIDATION"] = "1"

# Import tier enforcement system
from crystalline.licensing import (
    check_tier_access,
    get_tier,
    is_tier_1_only,
)

# Log tier information on import
_tier_info = get_tier()
if _tier_info not in ["TIER_1_FREE", "TIER_1"]:
    warnings.warn(
        f"WARNING: Crystalline-tier1 is Tier 1 (CPU-only). "
        f"Higher tier features (GPU, Champion Mode) are not available. "
        f"For GPU acceleration, please purchase Tier 2+ at https://[DOMAIN]/tiers",
        RuntimeWarning,
        stacklevel=2
    )

# Core API exports
from crystalline.api import (
    get_backend,
    spectral_analysis,
    spectral_filtering,
)

# Public functions that are Tier 1 safe
def get_backend():
    """Get the Tier 1 CPU backend.
    
    Returns CPU-based backend suitable for learning and research.
    GPU acceleration available in Tier 2+.
    """
    from crystalline.backend import get_backend as _get_backend
    return _get_backend()

# Tier 1 info
def get_tier_info():
    """Get current tier information."""
    return {
        "tier": "TIER_1_FREE",
        "version": __version__,
        "gpu_available": False,
        "champion_mode_available": False,
        "jit_available": False,
        "description": "Free, open-source CPU-only edition",
    }

# Override any system-level tier checks
def _enforce_tier_1():
    """Enforce that only Tier 1 features are accessible."""
    # This runs at import time
    check_tier_access("spectral_analysis")  # Only allow Tier 1+ features

_enforce_tier_1()

__all__ = [
    "get_backend",
    "spectral_analysis",
    "spectral_filtering",
    "get_tier_info",
    "__version__",
    "__tier__",
]
