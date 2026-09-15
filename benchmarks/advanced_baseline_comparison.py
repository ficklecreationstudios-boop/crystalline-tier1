"""Reproducible baseline comparison for Tier 1 operations.

The benchmark deliberately compares equivalent mathematical operations. A raw
NumPy FFT is not treated as a baseline for Crystalline's PSD API because it
omits windowing, density normalization, and one-sided PSD construction.

This script reports cold, warm, and stability timings. It does not assert that
Crystalline is faster than another implementation; results are evidence for a
specific environment only. The run metadata printed at startup records the
software versions, platform, random seed, and iteration counts needed to
interpret the timing evidence.
"""

import platform
import sys
import time
import warnings

import numpy as np
from scipy import signal

warnings.filterwarnings("ignore")

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


SEED = 42
WARM_RUNS = 20
STABILITY_RUNS = 50


class StabilityAnalyzer:
    """Analyze cold start, warm-up, and stability metrics."""

    def __init__(self, name, cold_time=None, warm_times=None, stability_times=None):
        self.name = name
        self.cold_time = cold_time
        self.warm_times = np.array(warm_times) if warm_times else np.array([])
        self.stability_times = np.array(stability_times) if stability_times else np.array([])

    def stats(self):
        """Compute summary statistics in milliseconds."""
        stability = self.stability_times
        return {
            "cold_start": self.cold_time,
            "warm_mean": np.mean(self.warm_times) if self.warm_times.size else None,
            "warm_std": np.std(self.warm_times) if self.warm_times.size else None,
            "stability_mean": np.mean(stability) if stability.size else None,
            "stability_std": np.std(stability) if stability.size else None,
            "stability_median": np.median(stability) if stability.size else None,
            "stability_p95": np.percentile(stability, 95) if stability.size else None,
            "stability_cv": (
                np.std(stability) / np.mean(stability) * 100
                if stability.size and np.mean(stability) > 0
                else None
            ),
        }

    def format_stats(self):
        s = self.stats()
        return {
            "Cold Start": f"{s['cold_start']:.3f} ms" if s["cold_start"] is not None else "N/A",
            "Warm Mean": f"{s['warm_mean']:.3f} ms" if s["warm_mean"] is not None else "N/A",
            "Warm Std": f"{s['warm_std']:.3f} ms" if s["warm_std"] is not None else "N/A",
            "Stability Median": (
                f"{s['stability_median']:.3f} ms"
                if s["stability_median"] is not None
                else "N/A"
            ),
            "Stability P95": (
                f"{s['stability_p95']:.3f} ms" if s["stability_p95"] is not None else "N/A"
            ),
            "Coefficient of Variation": (
                f"{s['stability_cv']:.1f}%" if s["stability_cv"] is not None else "N/A"
            ),
        }


def _measure(fn, warm_runs=WARM_RUNS, stability_runs=STABILITY_RUNS):
    start = time.perf_counter()
    fn()
    cold = (time.perf_counter() - start) * 1000

    warm = []
    for _ in range(warm_runs):
        start = time.perf_counter()
        fn()
        warm.append((time.perf_counter() - start) * 1000)

    stability = []
    for _ in range(stability_runs):
        start = time.perf_counter()
        fn()
        stability.append((time.perf_counter() - start) * 1000)

    return cold, warm, stability


def _print_results(results):
    print(
        f"\n{'Library':<28} {'Cold':<14} {'Warm Mean':<14} "
        f"{'Median':<14} {'P95':<14} {'CV':<10}"
    )
    print("-" * 100)
    for name, analyzer in results.items():
        s = analyzer.stats()
        print(
            f"{name:<28} {s['cold_start']:.3f} ms      "
            f"{s['warm_mean']:.3f} ms      {s['stability_median']:.3f} ms      "
            f"{s['stability_p95']:.3f} ms      {s['stability_cv']:.1f}%"
        )


def benchmark_spectral_psd():
    """Compare equivalent one-sided density-scaled PSD calculations."""
    print("\n" + "=" * 100)
    print("SPECTRAL PSD — EQUIVALENT SEMANTICS")
    print("=" * 100)

    from crystalline import spectral_analysis

    sizes = [1024, 10240, 102400]
    for size in sizes:
        print(f"\nArray Size: {size:,} samples")
        data = np.random.default_rng(SEED).normal(size=size).astype(np.float64)
        results = {}

        def scipy_psd():
            signal.periodogram(
                data,
                fs=1.0,
                window="hamming",
                detrend=False,
                scaling="density",
                return_onesided=True,
            )

        def crystalline_psd():
            spectral_analysis(data, fs=1.0, window="hamming")

        for name, fn in (
            ("SciPy periodogram", scipy_psd),
            ("Crystalline Tier 1", crystalline_psd),
        ):
            cold, warm, stability = _measure(fn)
            results[name] = StabilityAnalyzer(name, cold, warm, stability)

        if HAS_TORCH:
            # PyTorch's raw FFT is intentionally not included: it is not the
            # same operation as the density-scaled PSD API.
            print("PyTorch raw FFT omitted: different mathematical semantics.")

        _print_results(results)


def benchmark_matrix_multiplication():
    """Compare equivalent matrix multiplication operations."""
    print("\n" + "=" * 100)
    print("MATRIX MULTIPLICATION — EQUIVALENT SEMANTICS")
    print("=" * 100)

    from crystalline.backend import get_backend

    backend = get_backend()
    sizes = [256, 1024]

    for size in sizes:
        print(f"\nMatrix Size: {size}×{size}")
        rng = np.random.default_rng(SEED)
        A = rng.normal(size=(size, size)).astype(np.float64)
        B = rng.normal(size=(size, size)).astype(np.float64)
        results = {}

        candidates = [("NumPy matmul", lambda: np.matmul(A, B)),
                      ("Crystalline Tier 1", lambda: backend.matrix_multiply(A, B))]
        if HAS_TORCH:
            torch_A = torch.from_numpy(A)
            torch_B = torch.from_numpy(B)
            candidates.append(("PyTorch matmul", lambda: torch.matmul(torch_A, torch_B)))

        for name, fn in candidates:
            cold, warm, stability = _measure(fn)
            results[name] = StabilityAnalyzer(name, cold, warm, stability)

        _print_results(results)


if __name__ == "__main__":
    print("\nCRYSTALLINE TIER 1 — BASELINE COMPARISON")
    print("Timing is environment-specific evidence, not a blanket performance claim.")
    print(f"Python: {sys.version.split()[0]}")
    print(f"NumPy: {np.__version__}")
    print(f"SciPy: {signal.__version__ if hasattr(signal, '__version__') else 'see scipy.__version__'}")
    import scipy
    print(f"SciPy version: {scipy.__version__}")
    print(f"Platform: {platform.platform()}")
    print(f"Machine: {platform.machine()}")
    print(f"Random seed: {SEED}")
    print(f"Warm runs: {WARM_RUNS}; stability runs: {STABILITY_RUNS}")
    print(f"PyTorch available: {HAS_TORCH}")
    benchmark_spectral_psd()
    benchmark_matrix_multiplication()
    print("\nBenchmark complete.")
