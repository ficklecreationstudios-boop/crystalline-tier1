"""
Example 4: Tier Access and Feature Restrictions

This example shows how Tier 1 restricts access to higher-tier features
and how to handle the restrictions.
"""

import sys
from crystalline.licensing import (
    get_tier, 
    check_tier_access,
    TierFeatureBlockedError,
    get_license_info
)

print("🔐 Tier Access Control Example")
print("=" * 50)

# Check current tier
current_tier = get_tier()
print(f"Current Tier: {current_tier}")

# Get license info
license_info = get_license_info()
print(f"License Source: {license_info['source']}")
print(f"GPU Enabled: {license_info['gpu_enabled']}")

print("\n1️⃣  Allowed Features (Tier 1)")
print("-" * 50)

allowed_features = [
    "spectral_analysis",
    "spectral_filtering",
    "convolution",
    "linear_algebra",
]

for feature in allowed_features:
    try:
        check_tier_access(feature)
        print(f"  ✅ {feature}")
    except TierFeatureBlockedError as e:
        print(f"  ❌ {feature}: {str(e)[:50]}...")

print("\n2️⃣  Blocked Features (Require Higher Tiers)")
print("-" * 50)

blocked_features = [
    ("gpu_acceleration", "Tier 2+"),
    ("champion_mode", "Tier 4"),
    ("jit_compilation", "Tier 4"),
]

for feature, required_tier in blocked_features:
    try:
        check_tier_access(feature)
        print(f"  ✅ {feature}")
    except TierFeatureBlockedError as e:
        print(f"  ❌ {feature} (needs {required_tier})")
        print(f"     Message: {str(e)[:80]}...")

print("\n3️⃣  Exception Handling")
print("-" * 50)

print("Attempting to access GPU backend...")
try:
    from crystalline.backend import GPUBackend
    backend = GPUBackend()
except TierFeatureBlockedError as e:
    print(f"✅ Caught exception (expected):")
    print(f"   {e}")

print("\n4️⃣  Feature Matrix Tier 1")
print("-" * 50)

from crystalline.kernels import (
    list_available_kernels,
    list_unavailable_kernels
)

available = list_available_kernels()
unavailable = list_unavailable_kernels()

print(f"Available kernels ({len(available)}):")
for kernel in available:
    print(f"  ✓ {kernel}")

print(f"\nUnavailable (higher tiers) ({len(unavailable)}):")
for kernel, tier in unavailable.items():
    print(f"  ✗ {kernel} ({tier})")

print("\n💡 Key Points:")
print("   - Tier 1 is completely free and open-source")
print("   - Try to access higher-tier features → TierFeatureBlockedError")
print("   - License validation disabled for GPL-3.0 compliance")
print("   - GPU operations hardcoded to fail with helpful message")
print("   - For GPU: contact [SALES_EMAIL]")
