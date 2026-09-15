"""Independent checks for the published Tier 1 feature guard."""

import pytest

from crystalline.licensing import (
    TierFeatureBlockedError,
    check_tier_access,
    get_license_info,
    get_tier,
    is_tier_1_only,
)


def test_published_distribution_is_tier_1_regardless_of_environment(monkeypatch):
    monkeypatch.setenv("CRYSTALLINE_TIER", "TIER_4")

    assert get_tier() == "TIER_1_FREE"
    assert is_tier_1_only()


def test_supported_feature_is_allowed():
    assert check_tier_access("spectral_analysis") is True


def test_unavailable_feature_is_blocked():
    with pytest.raises(TierFeatureBlockedError):
        check_tier_access("gpu_acceleration")


def test_unknown_feature_is_blocked():
    with pytest.raises(TierFeatureBlockedError):
        check_tier_access("future_feature")


def test_license_info_matches_published_runtime():
    info = get_license_info()

    assert info["tier"] == "TIER_1_FREE"
    assert info["source"] == "Open Source (GPL-3.0)"
    assert info["gpu_enabled"] is False
