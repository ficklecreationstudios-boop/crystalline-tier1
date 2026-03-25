"""
Advanced Baseline Comparison - Cold Start + Stability Analysis

Tests all libraries (NumPy, SciPy, PyTorch, Crystalline) with:
- Cold start measurements
- Warm-up iterations
- Stability/variance analysis (50 runs)
- Coefficient of variation
"""

import numpy as np
import time
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

class StabilityAnalyzer:
    """Analyze cold start, warm-up, and stability metrics."""

    def __init__(self, name, cold_time=None, warm_times=None, stability_times=None):
        self.name = name
        self.cold_time = cold_time
        self.warm_times = np.array(warm_times) if warm_times else np.array([])
        self.stability_times = np.array(stability_times) if stability_times else np.array([])

    def stats(self):
        """Compute statistics."""
        return {
            'cold_start': self.cold_time,
            'warm_mean': np.mean(self.warm_times) if len(self.warm_times) > 0 else None,
            'warm_std': np.std(self.warm_times) if len(self.warm_times) > 0 else None,
            'stability_mean': np.mean(self.stability_times) if len(self.stability_times) > 0 else None,
            'stability_std': np.std(self.stability_times) if len(self.stability_times) > 0 else None,
            'stability_cv': (np.std(self.stability_times) / np.mean(self.stability_times) * 100) if len(self.stability_times) > 0 and np.mean(self.stability_times) > 0 else None,
        }

    def format_stats(self):
        """Format stats for display."""
        s = self.stats()
        return {
            'Cold Start': f"{s['cold_start']:.3f} ms" if s['cold_start'] else "N/A",
            'Warm Mean': f"{s['warm_mean']:.3f} ms" if s['warm_mean'] else "N/A",
            'Warm Std': f"{s['warm_std']:.3f} ms" if s['warm_std'] else "N/A",
            'Stability Mean': f"{s['stability_mean']:.3f} ms" if s['stability_mean'] else "N/A",
            'Stability Std': f"{s['stability_std']:.3f} ms" if s['stability_std'] else "N/A",
            'Coefficient of Variation': f"{s['stability_cv']:.1f}%" if s['stability_cv'] is not None else "N/A",
        }


def benchmark_spectral_fft():
    """Compare FFT performance across all libraries."""

    print("\n" + "="*100)
    print("🚀 SPECTRAL ANALYSIS (FFT) - COLD START + STABILITY COMPARISON")
    print("="*100)

    from crystalline import spectral_analysis as cryst_fft

    sizes = [1024, 10240, 102400]
    warm_runs = 20
    stability_runs = 50

    for size in sizes:
        print(f"\n📈 Array Size: {size:,} samples")
        print("-"*100)

        data = np.random.randn(size).astype(np.float64)
        results = {}

        # NumPy FFT (baseline)
        start = time.perf_counter()
        np.fft.fft(data)
        cold_numpy = (time.perf_counter() - start) * 1000

        warm_times = []
        for _ in range(warm_runs):
            start = time.perf_counter()
            np.fft.fft(data)
            warm_times.append((time.perf_counter() - start) * 1000)

        stability_times = []
        for _ in range(stability_runs):
            start = time.perf_counter()
            np.fft.fft(data)
            stability_times.append((time.perf_counter() - start) * 1000)

        results['NumPy FFT'] = StabilityAnalyzer('NumPy', cold_numpy, warm_times, stability_times)

        # SciPy Periodogram (old approach)
        start = time.perf_counter()
        signal.periodogram(data)
        cold_scipy = (time.perf_counter() - start) * 1000

        warm_times = []
        for _ in range(warm_runs):
            start = time.perf_counter()
            signal.periodogram(data)
            warm_times.append((time.perf_counter() - start) * 1000)

        stability_times = []
        for _ in range(stability_runs):
            start = time.perf_counter()
            signal.periodogram(data)
            stability_times.append((time.perf_counter() - start) * 1000)

        results['SciPy Periodogram'] = StabilityAnalyzer('SciPy', cold_scipy, warm_times, stability_times)

        # PyTorch FFT (if available)
        if HAS_TORCH:
            torch_data = torch.from_numpy(data)
            start = time.perf_counter()
            torch.fft.fft(torch_data)
            cold_torch = (time.perf_counter() - start) * 1000

            warm_times = []
            for _ in range(warm_runs):
                start = time.perf_counter()
                torch.fft.fft(torch_data)
                warm_times.append((time.perf_counter() - start) * 1000)

            stability_times = []
            for _ in range(stability_runs):
                start = time.perf_counter()
                torch.fft.fft(torch_data)
                stability_times.append((time.perf_counter() - start) * 1000)

            results['PyTorch FFT'] = StabilityAnalyzer('PyTorch', cold_torch, warm_times, stability_times)

        # Crystalline Tier 1 (optimized)
        start = time.perf_counter()
        cryst_fft(data)
        cold_cryst = (time.perf_counter() - start) * 1000

        warm_times = []
        for _ in range(warm_runs):
            start = time.perf_counter()
            cryst_fft(data)
            warm_times.append((time.perf_counter() - start) * 1000)

        stability_times = []
        for _ in range(stability_runs):
            start = time.perf_counter()
            cryst_fft(data)
            stability_times.append((time.perf_counter() - start) * 1000)

        results['Crystalline Tier 1'] = StabilityAnalyzer('Crystalline', cold_cryst, warm_times, stability_times)

        # Display results
        print(f"\n{'Library':<25} {'Cold Start':<15} {'Warm Mean':<15} {'Warm Std':<15} {'Stab. CV':<12}")
        print("-"*100)

        for lib_name, analyzer in results.items():
            fmt = analyzer.format_stats()
            cv = analyzer.stats()['stability_cv']
            cv_str = f"{cv:.1f}%" if cv is not None else "N/A"
            print(f"{lib_name:<25} {fmt['Cold Start']:<15} {fmt['Warm Mean']:<15} {fmt['Warm Std']:<15} {cv_str:<12}")

        # Performance analysis
        print(f"\n📊 Performance Analysis:")
        baseline_warm = results['NumPy FFT'].stats()['warm_mean']
        for lib_name, analyzer in results.items():
            if lib_name != 'NumPy FFT':
                warm = analyzer.stats()['warm_mean']
                ratio = baseline_warm / warm
                symbol = "✓" if ratio >= 0.9 else "⚠"
                print(f"  {symbol} {lib_name}: {ratio:.2f}x vs NumPy")


def benchmark_matrix_multiplication():
    """Compare matrix multiplication performance."""

    print("\n" + "="*100)
    print("⚡ MATRIX MULTIPLICATION - COLD START + STABILITY COMPARISON")
    print("="*100)

    from crystalline.backend import get_backend
    backend = get_backend()

    sizes = [256, 1024]
    warm_runs = 20
    stability_runs = 50

    for size in sizes:
        print(f"\n📈 Matrix Size: {size}×{size}")
        print("-"*100)

        np.random.seed(42)
        A = np.random.randn(size, size).astype(np.float64)
        B = np.random.randn(size, size).astype(np.float64)
        results = {}

        # NumPy
        start = time.perf_counter()
        np.matmul(A, B)
        cold_numpy = (time.perf_counter() - start) * 1000

        warm_times = []
        for _ in range(warm_runs):
            start = time.perf_counter()
            np.matmul(A, B)
            warm_times.append((time.perf_counter() - start) * 1000)

        stability_times = []
        for _ in range(stability_runs):
            start = time.perf_counter()
            np.matmul(A, B)
            stability_times.append((time.perf_counter() - start) * 1000)

        results['NumPy matmul'] = StabilityAnalyzer('NumPy', cold_numpy, warm_times, stability_times)

        # PyTorch (if available)
        if HAS_TORCH:
            torch_A = torch.from_numpy(A)
            torch_B = torch.from_numpy(B)
            start = time.perf_counter()
            torch.matmul(torch_A, torch_B)
            cold_torch = (time.perf_counter() - start) * 1000

            warm_times = []
            for _ in range(warm_runs):
                start = time.perf_counter()
                torch.matmul(torch_A, torch_B)
                warm_times.append((time.perf_counter() - start) * 1000)

            stability_times = []
            for _ in range(stability_runs):
                start = time.perf_counter()
                torch.matmul(torch_A, torch_B)
                stability_times.append((time.perf_counter() - start) * 1000)

            results['PyTorch matmul'] = StabilityAnalyzer('PyTorch', cold_torch, warm_times, stability_times)

        # Crystalline
        start = time.perf_counter()
        backend.matrix_multiply(A, B)
        cold_cryst = (time.perf_counter() - start) * 1000

        warm_times = []
        for _ in range(warm_runs):
            start = time.perf_counter()
            backend.matrix_multiply(A, B)
            warm_times.append((time.perf_counter() - start) * 1000)

        stability_times = []
        for _ in range(stability_runs):
            start = time.perf_counter()
            backend.matrix_multiply(A, B)
            stability_times.append((time.perf_counter() - start) * 1000)

        results['Crystalline Tier 1'] = StabilityAnalyzer('Crystalline', cold_cryst, warm_times, stability_times)

        # Display results
        print(f"\n{'Library':<25} {'Cold Start':<15} {'Warm Mean':<15} {'Warm Std':<15} {'Stab. CV':<12}")
        print("-"*100)

        for lib_name, analyzer in results.items():
            fmt = analyzer.format_stats()
            cv = analyzer.stats()['stability_cv']
            cv_str = f"{cv:.1f}%" if cv is not None else "N/A"
            print(f"{lib_name:<25} {fmt['Cold Start']:<15} {fmt['Warm Mean']:<15} {fmt['Warm Std']:<15} {cv_str:<12}")

        # Performance analysis
        print(f"\n📊 Performance Analysis:")
        baseline_warm = results['NumPy matmul'].stats()['warm_mean']
        for lib_name, analyzer in results.items():
            if lib_name != 'NumPy matmul':
                warm = analyzer.stats()['warm_mean']
                ratio = baseline_warm / warm
                symbol = "✓" if ratio >= 0.95 else "⚠"
                print(f"  {symbol} {lib_name}: {ratio:.2f}x vs NumPy")


if __name__ == "__main__":
    print("\n🔍 CRYSTALLINE TIER 1 - ADVANCED BASELINE COMPARISON")
    print("Testing with: Cold Start + Warm-up + Stability (50 runs)")

    benchmark_spectral_fft()
    benchmark_matrix_multiplication()

    print("\n" + "="*100)
    print("✅ Advanced baseline comparison complete!")
    print("="*100)
