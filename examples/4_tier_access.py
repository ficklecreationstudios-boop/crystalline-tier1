"""Example 4: inspect the published Tier 1 feature inventory.

This example demonstrates how to distinguish implemented CPU operations from
features that are not implemented by this distribution.
"""

from crystalline.kernels import list_available_kernels, list_unavailable_kernels
from crystalline.licensing import (
    TierFeatureBlockedError,
    check_tier_access,
    get_license_info,
    get_tier,
)

print("Tier 1 Feature Availability")
print("=" * 50)

print(f"Published tier: {get_tier()}")
license_info = get_license_info()
print(f"License: {license_info['source']}")
print(f"GPU enabled: {license_info['gpu_enabled']}")

print("\n1. Implemented feature groups")
print("-" * 50)
for feature in [
    "spectral_analysis",
    "spectral_filtering",
    "convolution",
    "linear_algebra",
]:
    try:
        check_tier_access(feature)
        print(f"  OK  {feature}")
    except TierFeatureBlockedError as exc:
        print(f"  NO  {feature}: {exc}")

print("\n2. Kernel inventory")
print("-" * 50)
for kernel in list_available_kernels():
    print(f"  OK  {kernel}")

print("\n3. Features not implemented by this distribution")
print("-" * 50)
for feature, reason in list_unavailable_kernels().items():
    print(f"  NO  {feature}: {reason}")

print("\n4. GPU access")
print("-" * 50)
try:
    from crystalline.backend import GPUBackend

    GPUBackend()
except TierFeatureBlockedError as exc:
    print(f"  Expected block: {exc}")

print(
    "\nThis inventory describes current implementation availability; "
    "it does not promise higher-tier products, pricing, or performance."
)
