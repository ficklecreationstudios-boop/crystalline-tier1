"""Independent checks for the published kernel inventory."""

from crystalline.backend import CPUBackend
from crystalline.kernels import (
    AVAILABLE_KERNELS_TIER1,
    UNAVAILABLE_KERNELS_HIGHER_TIERS,
    list_available_kernels,
    list_unavailable_kernels,
)


def test_available_kernel_inventory_matches_cpu_backend_methods():
    backend = CPUBackend()
    expected = {
        "spectral_analysis",
        "spectral_filtering",
        "convolution",
        "linear_algebra_solve",
        "matrix_multiply",
    }

    assert set(AVAILABLE_KERNELS_TIER1) == expected
    assert all(callable(getattr(backend, name)) for name in AVAILABLE_KERNELS_TIER1)


def test_kernel_inventory_does_not_advertise_stale_operations():
    stale_names = {
        "correlation",
        "fft",
        "ifft",
        "matrix_solve",
        "qr_decomposition",
        "svd_decomposition",
    }

    assert stale_names.isdisjoint(AVAILABLE_KERNELS_TIER1)


def test_kernel_inventory_accessors_return_copies():
    available = list_available_kernels()
    unavailable = list_unavailable_kernels()

    available.append("not_a_real_kernel")
    unavailable["not_a_real_feature"] = "not implemented"

    assert "not_a_real_kernel" not in AVAILABLE_KERNELS_TIER1
    assert "not_a_real_feature" not in UNAVAILABLE_KERNELS_HIGHER_TIERS


def test_unavailable_inventory_has_no_commercial_tier_promises():
    assert all(
        reason in {"not implemented", "not implemented in Tier 1"}
        for reason in UNAVAILABLE_KERNELS_HIGHER_TIERS.values()
    )
