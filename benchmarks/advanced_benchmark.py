"""
Advanced Benchmark Suite for Crystalline GPU Tier 1

Comprehensive testing including:
- Cold start (first call overhead)
- Warm up (cached JIT compilation)
- Stability metrics (variance, std dev)
- All operation categories
- Multiple array sizes
- Performance profiling
"""

import numpy as np
import time
import json
from datetime import datetime
from scipy import signal
import warnings
from typing import Dict, List, Tuple

# Suppress warnings for clean output
warnings.filterwarnings('ignore')

class AdvancedBenchmarkTimer:
    """High-precision timer with cold/warm tracking."""

    def __init__(self):
        self.times = []
        self.cold_start = None
        self.warm_times = []

    def measure_cold_start(self, func, *args, **kwargs):
        """Measure first call (cold start)."""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        self.cold_start = elapsed
        return result, elapsed

    def measure_warm(self, func, iterations: int, *args, **kwargs):
        """Measure after warm-up (JIT compiled)."""
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            times.append((time.perf_counter() - start) * 1000)
        self.warm_times = times
        return np.array(times)

    def stats(self) -> Dict:
        """Compute statistics."""
        if not self.warm_times:
            return {}

        warm = np.array(self.warm_times)
        return {
            'cold_start': self.cold_start,
            'warm_mean': np.mean(warm),
            'warm_std': np.std(warm),
            'warm_min': np.min(warm),
            'warm_max': np.max(warm),
            'warm_median': np.median(warm),
            'coefficient_of_variation': np.std(warm) / np.mean(warm) if np.mean(warm) > 0 else 0,
        }


class AdvancedBenchmarkSuite:
    """Comprehensive benchmark suite with stability testing."""

    def __init__(self):
        self.results = {}
        self.config = {
            'cold_start_runs': 1,
            'warm_up_runs': 20,
            'stability_runs': 50,
            'array_sizes_fft': [1024, 10240, 102400, 1024000],
            'matrix_sizes': [64, 256, 1024],
            'filter_sizes': [1024, 10240, 102400, 1024000],
            'conv_sizes': [1024, 10240, 102400],
        }

    def generate_test_data(self, size: int) -> np.ndarray:
        """Generate random test data."""
        np.random.seed(42)  # For reproducibility
        return np.random.randn(size).astype(np.float64)

    def generate_matrix_pair(self, size: int) -> Tuple[np.ndarray, np.ndarray]:
        """Generate matrix pair for multiplication."""
        np.random.seed(42)
        A = np.random.randn(size, size).astype(np.float64)
        B = np.random.randn(size, size).astype(np.float64)
        return A, B

    def benchmark_spectral_analysis(self):
        """Benchmark FFT across all sizes."""
        print("\n" + "="*80)
        print("📊 ADVANCED FFT BENCHMARKS (Cold Start + Stability)")
        print("="*80)

        from crystalline import spectral_analysis
        import numpy as np_baseline

        results = {}

        for size in self.config['array_sizes_fft']:
            data = self.generate_test_data(size)
            timer = AdvancedBenchmarkTimer()

            print(f"\n📈 Array Size: {size:,} samples")
            print("-" * 80)

            # Cold start
            _, cold_time = timer.measure_cold_start(spectral_analysis, data)
            print(f"  🥶 Cold Start: {cold_time:.3f} ms")

            # Warm up iterations
            warm_times = timer.measure_warm(spectral_analysis, self.config['warm_up_runs'], data)

            # Stability test (after warm-up)
            stability_times = timer.measure_warm(spectral_analysis, self.config['stability_runs'], data)

            # NumPy baseline (warm)
            np_times = []
            for _ in range(self.config['warm_up_runs']):
                start = time.perf_counter()
                np_baseline.fft.fft(data)
                np_times.append((time.perf_counter() - start) * 1000)

            stats = timer.stats()
            stats['numpy_mean'] = np.mean(np_times)
            stats['stability_std'] = np.std(stability_times)
            stats['stability_cv'] = np.std(stability_times) / np.mean(stability_times)

            results[size] = stats

            print(f"  ✓ Warm Mean: {stats['warm_mean']:.3f} ms")
            print(f"  ✓ Stability Std: {stats['stability_std']:.3f} ms")
            print(f"  ✓ Coefficient of Variation: {stats['stability_cv']:.1%}")
            print(f"  ✓ vs NumPy: {stats['numpy_mean']/stats['warm_mean']:.2f}x")

        self.results['spectral_analysis'] = results
        return results

    def benchmark_filtering(self):
        """Benchmark signal filtering."""
        print("\n" + "="*80)
        print("🔧 ADVANCED FILTERING BENCHMARKS (Cold Start + Stability)")
        print("="*80)

        from crystalline.backend import get_backend
        backend = get_backend()

        results = {}

        for size in self.config['filter_sizes']:
            data = self.generate_test_data(size)
            timer = AdvancedBenchmarkTimer()

            print(f"\n📈 Array Size: {size:,} samples")
            print("-" * 80)

            # Cold start
            _, cold_time = timer.measure_cold_start(
                backend.spectral_filtering, data, cutoff=0.5
            )
            print(f"  🥶 Cold Start: {cold_time:.3f} ms")

            # Warm up
            warm_times = timer.measure_warm(
                self.config['warm_up_runs'],
                backend.spectral_filtering, data, cutoff=0.5
            )

            # Stability test
            stability_times = []
            for _ in range(self.config['stability_runs']):
                start = time.perf_counter()
                backend.spectral_filtering(data, cutoff=0.5)
                stability_times.append((time.perf_counter() - start) * 1000)

            # SciPy baseline
            scipy_times = []
            for _ in range(self.config['warm_up_runs']):
                start = time.perf_counter()
                signal.butter(4, 0.5)
                signal.filtfilt(np.random.randn(2), np.random.randn(2), data)
                scipy_times.append((time.perf_counter() - start) * 1000)

            stats = {
                'cold_start': cold_time,
                'warm_mean': np.mean(warm_times) if len(warm_times) > 0 else 0,
                'warm_std': np.std(warm_times) if len(warm_times) > 0 else 0,
                'stability_std': np.std(stability_times),
                'stability_cv': np.std(stability_times) / np.mean(stability_times) if np.mean(stability_times) > 0 else 0,
                'scipy_mean': np.mean(scipy_times),
            }

            results[size] = stats

            print(f"  ✓ Warm Mean: {stats['warm_mean']:.3f} ms")
            print(f"  ✓ Stability Std: {stats['stability_std']:.3f} ms")
            print(f"  ✓ Coefficient of Variation: {stats['stability_cv']:.1%}")
            print(f"  ✓ vs SciPy: {stats['scipy_mean']/stats['warm_mean']:.2f}x")

        self.results['filtering'] = results
        return results

    def benchmark_matrix_multiplication(self):
        """Benchmark matrix multiplication."""
        print("\n" + "="*80)
        print("⚡ ADVANCED MATRIX MULTIPLICATION BENCHMARKS")
        print("="*80)

        from crystalline.backend import get_backend
        backend = get_backend()

        results = {}

        for size in self.config['matrix_sizes']:
            A, B = self.generate_matrix_pair(size)
            timer = AdvancedBenchmarkTimer()

            print(f"\n📈 Matrix Size: {size}×{size}")
            print("-" * 80)

            # Cold start
            _, cold_time = timer.measure_cold_start(backend.matrix_multiply, A, B)
            print(f"  🥶 Cold Start: {cold_time:.3f} ms")

            # Warm up
            warm_times = timer.measure_warm(
                self.config['warm_up_runs'],
                backend.matrix_multiply, A, B
            )

            # Stability test
            stability_times = []
            for _ in range(self.config['stability_runs']):
                start = time.perf_counter()
                backend.matrix_multiply(A, B)
                stability_times.append((time.perf_counter() - start) * 1000)

            # NumPy baseline
            np_times = []
            for _ in range(self.config['warm_up_runs']):
                start = time.perf_counter()
                np.matmul(A, B)
                np_times.append((time.perf_counter() - start) * 1000)

            stats = {
                'cold_start': cold_time,
                'warm_mean': np.mean(warm_times),
                'warm_std': np.std(warm_times),
                'stability_std': np.std(stability_times),
                'stability_cv': np.std(stability_times) / np.mean(stability_times),
                'numpy_mean': np.mean(np_times),
            }

            results[size] = stats

            print(f"  ✓ Warm Mean: {stats['warm_mean']:.3f} ms")
            print(f"  ✓ Stability Std: {stats['stability_std']:.3f} ms")
            print(f"  ✓ Coefficient of Variation: {stats['stability_cv']:.1%}")
            print(f"  ✓ vs NumPy: {stats['numpy_mean']/stats['warm_mean']:.2f}x")

        self.results['matrix_multiply'] = results
        return results

    def benchmark_linear_solve(self):
        """Benchmark linear system solving."""
        print("\n" + "="*80)
        print("🔍 ADVANCED LINEAR SOLVE BENCHMARKS")
        print("="*80)

        from crystalline.backend import get_backend
        from scipy import linalg
        backend = get_backend()

        results = {}

        for size in self.config['matrix_sizes']:
            A, _ = self.generate_matrix_pair(size)
            b = self.generate_test_data(size)
            timer = AdvancedBenchmarkTimer()

            print(f"\n📈 System Size: {size}×{size}")
            print("-" * 80)

            # Cold start
            _, cold_time = timer.measure_cold_start(backend.linear_algebra_solve, A, b)
            print(f"  🥶 Cold Start: {cold_time:.3f} ms")

            # Warm up
            warm_times = timer.measure_warm(
                self.config['warm_up_runs'],
                backend.linear_algebra_solve, A, b
            )

            # Stability test
            stability_times = []
            for _ in range(self.config['stability_runs']):
                start = time.perf_counter()
                backend.linear_algebra_solve(A, b)
                stability_times.append((time.perf_counter() - start) * 1000)

            # SciPy baseline
            scipy_times = []
            for _ in range(self.config['warm_up_runs']):
                start = time.perf_counter()
                linalg.solve(A, b)
                scipy_times.append((time.perf_counter() - start) * 1000)

            stats = {
                'cold_start': cold_time,
                'warm_mean': np.mean(warm_times),
                'warm_std': np.std(warm_times),
                'stability_std': np.std(stability_times),
                'stability_cv': np.std(stability_times) / np.mean(stability_times),
                'scipy_mean': np.mean(scipy_times),
            }

            results[size] = stats

            print(f"  ✓ Warm Mean: {stats['warm_mean']:.3f} ms")
            print(f"  ✓ Stability Std: {stats['stability_std']:.3f} ms")
            print(f"  ✓ Coefficient of Variation: {stats['stability_cv']:.1%}")
            print(f"  ✓ vs SciPy: {stats['scipy_mean']/stats['warm_mean']:.2f}x")

        self.results['linear_solve'] = results
        return results

    def benchmark_convolution(self):
        """Benchmark 1D convolution."""
        print("\n" + "="*80)
        print("🌊 ADVANCED CONVOLUTION BENCHMARKS")
        print("="*80)

        from crystalline.backend import get_backend
        backend = get_backend()

        results = {}
        kernel = np.array([0.2, 0.5, 0.2, 0.1, 0.0, -0.1, -0.2])

        for size in self.config['conv_sizes']:
            data = self.generate_test_data(size)
            timer = AdvancedBenchmarkTimer()

            print(f"\n📈 Array Size: {size:,} samples")
            print("-" * 80)

            # Cold start
            _, cold_time = timer.measure_cold_start(backend.convolution, data, kernel)
            print(f"  🥶 Cold Start: {cold_time:.3f} ms")

            # Warm up
            warm_times = timer.measure_warm(
                self.config['warm_up_runs'],
                backend.convolution, data, kernel
            )

            # Stability test
            stability_times = []
            for _ in range(self.config['stability_runs']):
                start = time.perf_counter()
                backend.convolution(data, kernel)
                stability_times.append((time.perf_counter() - start) * 1000)

            # SciPy baseline
            scipy_times = []
            for _ in range(self.config['warm_up_runs']):
                start = time.perf_counter()
                signal.convolve(data, kernel, mode='same')
                scipy_times.append((time.perf_counter() - start) * 1000)

            stats = {
                'cold_start': cold_time,
                'warm_mean': np.mean(warm_times),
                'warm_std': np.std(warm_times),
                'stability_std': np.std(stability_times),
                'stability_cv': np.std(stability_times) / np.mean(stability_times),
                'scipy_mean': np.mean(scipy_times),
            }

            results[size] = stats

            print(f"  ✓ Warm Mean: {stats['warm_mean']:.3f} ms")
            print(f"  ✓ Stability Std: {stats['stability_std']:.3f} ms")
            print(f"  ✓ Coefficient of Variation: {stats['stability_cv']:.1%}")
            print(f"  ✓ vs SciPy: {stats['scipy_mean']/stats['warm_mean']:.2f}x")

        self.results['convolution'] = results
        return results

    def run_all(self):
        """Run all benchmarks."""
        print("\n" + "="*80)
        print("🚀 CRYSTALLINE TIER 1 - ADVANCED BENCHMARK SUITE")
        print("="*80)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Configuration: {self.config}")

        self.benchmark_spectral_analysis()
        self.benchmark_filtering()
        self.benchmark_matrix_multiplication()
        self.benchmark_linear_solve()
        self.benchmark_convolution()

        print("\n" + "="*80)
        print("✅ BENCHMARK SUITE COMPLETED")
        print("="*80)

        # Save results
        self.save_results()

        return self.results

    def save_results(self):
        """Save results to JSON."""
        filename = f"advanced_benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📁 Results saved to: {filename}")


if __name__ == "__main__":
    suite = AdvancedBenchmarkSuite()
    results = suite.run_all()
