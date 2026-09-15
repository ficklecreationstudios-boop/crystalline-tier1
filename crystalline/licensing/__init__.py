"""Feature availability for the published Tier 1 distribution.

This module is a feature-availability guard, not a security boundary or a
commercial license server. The repository currently ships only the Tier 1
CPU implementation, so this distribution reports Tier 1 consistently.
"""


class Tier1EnforcementError(Exception):
    """Raised when a Tier 1 feature request cannot be satisfied."""


class TierFeatureBlockedError(Tier1EnforcementError):
    """Raised when a feature is unavailable in the published Tier 1 build."""


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
    """Return the tier implemented by this distribution."""
    return "TIER_1_FREE"


def check_tier_access(feature_name):
    """Check whether ``feature_name`` is implemented in Tier 1.

    Unknown features and explicitly unavailable features are blocked. This is
    an application-level feature guard; it does not provide security against a
    modified copy of the source code.
    """
    features = TIER_FEATURES["TIER_1_FREE"]
    if feature_name not in features or not features[feature_name]:
        raise TierFeatureBlockedError(
            f"Feature '{feature_name}' is not available in the published Tier 1 build."
        )
    return True


def enforce_tier_access(feature_name):
    """Alias for :func:`check_tier_access`."""
    return check_tier_access(feature_name)


def is_tier_1_only():
    """Return whether this distribution implements only Tier 1 features."""
    return True


def get_license_info():
    """Return factual license and runtime information for this distribution."""
    return {
        "tier": "TIER_1_FREE",
        "licensed": True,
        "source": "Open Source (GPL-3.0)",
        "expiration": None,
        "gpu_enabled": False,
        "gpu_operations": 0,
    }


def validate_license():
    """Return True for the repository's declared open-source license."""
    return True


def check_feature(feature_name):
    """Alias for :func:`check_tier_access`."""
    return check_tier_access(feature_name)


class LicenseValidator:
    """Compatibility wrapper for the open-source Tier 1 distribution."""

    def validate(self):
        """Return True; no external license server is required."""
        return True

    def get_tier(self):
        """Return the implemented distribution tier."""
        return get_tier()


class LicenseError(Exception):
    """Base license-related compatibility exception."""


class LicenseInvalidError(LicenseError):
    """Compatibility exception for an invalid license."""


class LicenseExpiredError(LicenseInvalidError):
    """Compatibility exception for an expired license."""


__all__ = [
    "Tier1EnforcementError",
    "TierFeatureBlockedError",
    "LicenseError",
    "LicenseInvalidError",
    "LicenseExpiredError",
    "get_tier",
    "check_tier_access",
    "enforce_tier_access",
    "is_tier_1_only",
    "get_license_info",
    "validate_license",
    "check_feature",
    "LicenseValidator",
]
