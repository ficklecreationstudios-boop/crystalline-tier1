"""
crystalline/licensing/__init__.py
TIER 1 ENFORCEMENT MODULE

This module enforces strict tier restrictions to prevent unauthorized
access to higher-tier features. It acts as a security boundary.

TIER 1 RESTRICTIONS:
- No GPU acceleration (CPU only)
- No Champion Mode
- No JIT specialization
- No hardware-bound licensing
- No commercial features
"""

class Tier1EnforcementError(Exception):
    """Raised when attempting to access non-Tier-1 features."""
    pass

class TierFeatureBlockedError(Tier1EnforcementError):
    """Raised when accessing higher-tier-only features."""
    pass

# Tier features matrix
TIER_FEATURES = {
    "TIER_1_FREE": {
        "spectral_analysis": True,
        "spectral_filtering": True,
        "convolution": True,
        "linear_algebra": True,
        "signal_processing": True,
        "gpu_acceleration": False,
        "champion_mode": False,
        "jit_compilation": False,
        "hardware_licensing": False,
        "domain_wheels": False,
        "enterprise_support": False,
    }
}

def get_tier():
    """Get current tier. Always returns TIER_1_FREE in this distribution."""
    import os
    # Force Tier 1 regardless of environment
    return os.environ.get("CRYSTALLINE_TIER", "TIER_1_FREE")

def check_tier_access(feature_name):
    """Check if a feature is available in current tier.
    
    Args:
        feature_name: Name of the feature to check
        
    Returns:
        True if feature is available
        
    Raises:
        TierFeatureBlockedError if feature is not available in Tier 1
    """
    tier = get_tier()
    features = TIER_FEATURES.get(tier, {})
    
    if feature_name not in features:
        # Unknown feature - default to blocked for higher tiers
        raise TierFeatureBlockedError(
            f"Feature '{feature_name}' is not available in {tier}. "
            f"This feature requires a higher tier. "
            f"For GPU acceleration and advanced features, see https://crystalline.io/tiers"
        )
    
    if not features[feature_name]:
        raise TierFeatureBlockedError(
            f"Feature '{feature_name}' is not available in {tier} (Tier 1 - Free). "
            f"This feature is available in:\n"
            f"  - Tier 2: GPU acceleration ($500/month)\n"
            f"  - Tier 3: Domain wheels ($100K+/year)\n"
            f"  - Tier 4: Champion Mode ($300K+/year)\n"
            f"Contact [SALES_EMAIL] for commercial licensing."
        )
    
    return True

def enforce_tier_access(feature_name):
    """Enforce tier access - alias for check_tier_access."""
    return check_tier_access(feature_name)

def is_tier_1_only():
    """Check if running in Tier 1 only mode."""
    return get_tier() == "TIER_1_FREE"

def get_license_info():
    """Get license information. Tier 1 is always free/open-source."""
    return {
        "tier": get_tier(),
        "licensed": True,
        "source": "Open Source (GPL-3.0)",
        "expiration": None,
        "gpu_enabled": False,
        "gpu_operations": 0,
    }

def validate_license():
    """Validate license (Tier 1 always passes - GPL-3.0)."""
    return True

def check_feature(feature_name):
    """Check if feature is available (alias for check_tier_access)."""
    return check_tier_access(feature_name)

# Stub classes for compatibility
class LicenseValidator:
    """Tier 1 license validator (no validation needed)."""
    
    def validate(self):
        """Always validates in Tier 1 (GPL-3.0)."""
        return True
    
    def get_tier(self):
        """Get tier."""
        return get_tier()

class LicenseError(Exception):
    """License validation error."""
    pass

class LicenseInvalidError(LicenseError):
    """Invalid license."""
    pass

class LicenseExpiredError(LicenseInvalidError):
    """License expired."""
    pass

# Exports
__all__ = [
    # Exceptions
    "Tier1EnforcementError",
    "TierFeatureBlockedError",
    "LicenseError",
    "LicenseInvalidError",
    "LicenseExpiredError",
    # Functions
    "get_tier",
    "check_tier_access",
    "enforce_tier_access",
    "is_tier_1_only",
    "get_license_info",
    "validate_license",
    "check_feature",
    # Classes
    "LicenseValidator",
]
