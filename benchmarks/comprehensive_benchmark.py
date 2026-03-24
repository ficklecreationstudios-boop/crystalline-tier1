"""
Crystalline GPU Tier 1 - Benchmark Suite
==========================================

Comprehensive benchmarks comparing Tier 1 CPU-based operations against:
1. NumPy (baseline)
2. SciPy
3. Scikit-learn
4. PyTorch (CPU)
5. TensorFlow (CPU)

Operations tested:
- Spectral Analysis (FFT)
- Signal Filtering
- Matrix Multiplication
- Linear System Solving
- Convolution
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import numpy as np
from typing import Dict, List, Tuple
import json
from scipy import signal, linalg, fft
import warnings

warnings.filterwarnings('ignore')

# Benchmark configuration
class BenchmarkConfig:
    """Configuration for benchmarks."""
    
    ITERATIONS = 10
    WARMUP_RUNS = 2
    ARRAY_SIZES = [1024, 10240, 102400]
    MATRIX_SIZES = [64, 256, 1024]
    
    # Competitors
    COMPETITORS = [
        "NumPy",
        "SciPy",
        "Scikit-learn",
        "PyTorch (CPU)",
        "TensorFlow (CPU)",
    ]


class BenchmarkTimer:
    """High-precision timer for benchmarks."""
    
    def __init__(self):
        self.times = []
        self.start_time = None
    
    def start(self):
        """Start timer."""
        self.start_time = time.perf_counter()
    
    def stop(self) -> float:
        """Stop timer and return elapsed time in ms."""
        self.times.append((time.perf_counter() - self.start_time) * 1000)
        return self.times[-1]
    
    def mean(self) -> float:
        """Mean execution time in ms."""
        return np.mean(self.times)
    
    def std(self) -> float:
        """Standard deviation in ms."""
        return np.std(self.times)
    
    def median(self) -> float:
        """Median execution time in ms."""
        return np.median(self.times)
    
    def min(self) -> float:
        """Minimum execution time in ms."""
        return np.min(self.times)
    
    def max(self) -> float:
        """Maximum execution time in ms."""
        return np.max(self.times)


class CrystallineBenchmark:
    """Benchmark suite for Crystalline GPU Tier 1."""
    
    def __init__(self):
        self.results = {}
        self.config = BenchmarkConfig()
        self.backend = None
    
    def import_crystalline(self):
        """Import Crystalline GPU and get backend."""
        try:
            from crystalline import get_backend
            self.backend = get_backend()
            print("✅ Crystalline GPU Tier 1 imported successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to import Crystalline: {e}")
            return False
    
    def import_competitors(self) -> Dict[str, bool]:
        """Try to import all competitor libraries."""
        self.competitors = {}
        
        try:
            import scipy
            self.competitors['scipy'] = True
        except:
            self.competitors['scipy'] = False
        
        try:
            import sklearn
            self.competitors['sklearn'] = True
        except:
            self.competitors['sklearn'] = False
        
        try:
            import torch
            self.competitors['torch'] = True
        except:
            self.competitors['torch'] = False
        
        try:
            import tensorflow
            self.competitors['tensorflow'] = True
        except:
            self.competitors['tensorflow'] = False
        
        print("\n📦 Competitor Libraries:")
        for name, available in self.competitors.items():
            status = "✅" if available else "❌"
            print(f"   {status} {name.capitalize()}")
        
        return self.competitors
    
    def benchmark_spectral_analysis(self):
        """Benchmark spectral analysis (FFT-like operations)."""
        print("\n" + "="*70)
        print("TEST 1: SPECTRAL ANALYSIS (FFT)")
        print("="*70)
        
        results = {}
        
        for size in self.config.ARRAY_SIZES:
            print(f"\n📊 Array Size: {size:,} samples")
            print("-" * 70)
            
            # Generate test data
            data = np.random.randn(size).astype(np.float64)
            
            # BASELINE: NumPy FFT
            print("  NumPy (baseline)...", end=" ", flush=True)
            timer = BenchmarkTimer()
            for _ in range(self.config.WARMUP_RUNS):
                _ = np.fft.fft(data)
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = np.fft.fft(data)
                timer.stop()
            numpy_time = timer.mean()
            results[f"NumPy_{size}"] = numpy_time
            print(f"✓ {numpy_time:.3f}ms")
            
            # Crystalline Tier 1 (SciPy-backed)
            print("  Crystalline Tier 1...", end=" ", flush=True)
            timer = BenchmarkTimer()
            for _ in range(self.config.WARMUP_RUNS):
                _ = self.backend.spectral_analysis(data, fs=1.0)
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = self.backend.spectral_analysis(data, fs=1.0)
                timer.stop()
            crystalline_time = timer.mean()
            results[f"Crystalline_{size}"] = crystalline_time
            print(f"✓ {crystalline_time:.3f}ms")
            
            # SciPy Periodogram
            if self.competitors['scipy']:
                print("  SciPy periodogram...", end=" ", flush=True)
                timer = BenchmarkTimer()
                for _ in range(self.config.WARMUP_RUNS):
                    _ = signal.periodogram(data, fs=1.0)
                for _ in range(self.config.ITERATIONS):
                    timer.start()
                    _ = signal.periodogram(data, fs=1.0)
                    timer.stop()
                scipy_time = timer.mean()
                results[f"SciPy_{size}"] = scipy_time
                print(f"✓ {scipy_time:.3f}ms")
            
            # PyTorch FFT (CPU)
            if self.competitors['torch']:
                print("  PyTorch FFT (CPU)...", end=" ", flush=True)
                try:
                    import torch
                    data_torch = torch.from_numpy(data)
                    timer = BenchmarkTimer()
                    for _ in range(self.config.WARMUP_RUNS):
                        _ = torch.fft.fft(data_torch)
                    for _ in range(self.config.ITERATIONS):
                        timer.start()
                        _ = torch.fft.fft(data_torch)
                        timer.stop()
                    torch_time = timer.mean()
                    results[f"PyTorch_{size}"] = torch_time
                    print(f"✓ {torch_time:.3f}ms")
                except Exception as e:
                    print(f"✗ Error: {str(e)[:30]}")
            
            # TensorFlow FFT (CPU)
            if self.competitors['tensorflow']:
                print("  TensorFlow FFT (CPU)...", end=" ", flush=True)
                try:
                    import tensorflow as tf
                    data_tf = tf.constant(data, dtype=tf.complex128)
                    timer = BenchmarkTimer()
                    for _ in range(self.config.WARMUP_RUNS):
                        _ = tf.signal.fft(tf.cast(data_tf, tf.complex128))
                    for _ in range(self.config.ITERATIONS):
                        timer.start()
                        _ = tf.signal.fft(tf.cast(data_tf, tf.complex128))
                        timer.stop()
                    tf_time = timer.mean()
                    results[f"TensorFlow_{size}"] = tf_time
                    print(f"✓ {tf_time:.3f}ms")
                except Exception as e:
                    print(f"✗ Error: {str(e)[:30]}")
        
        self.results['spectral_analysis'] = results
        return results
    
    def benchmark_filtering(self):
        """Benchmark signal filtering."""
        print("\n" + "="*70)
        print("TEST 2: SIGNAL FILTERING (Butterworth Low-Pass)")
        print("="*70)
        
        results = {}
        
        for size in self.config.ARRAY_SIZES:
            print(f"\n📊 Array Size: {size:,} samples")
            print("-" * 70)
            
            # Generate test data
            data = np.random.randn(size).astype(np.float64)
            
            # BASELINE: SciPy Butterworth
            print("  SciPy Butterworth...", end=" ", flush=True)
            timer = BenchmarkTimer()
            b, a = signal.butter(4, 0.1)
            for _ in range(self.config.WARMUP_RUNS):
                _ = signal.filtfilt(b, a, data)
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = signal.filtfilt(b, a, data)
                timer.stop()
            scipy_time = timer.mean()
            results[f"SciPy_{size}"] = scipy_time
            print(f"✓ {scipy_time:.3f}ms (baseline)")
            
            # Crystalline Tier 1 (SciPy-backed)
            print("  Crystalline Tier 1...", end=" ", flush=True)
            timer = BenchmarkTimer()
            for _ in range(self.config.WARMUP_RUNS):
                _ = self.backend.spectral_filtering(data, cutoff=0.1, order=4, btype='low')
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = self.backend.spectral_filtering(data, cutoff=0.1, order=4, btype='low')
                timer.stop()
            crystalline_time = timer.mean()
            results[f"Crystalline_{size}"] = crystalline_time
            print(f"✓ {crystalline_time:.3f}ms")
            
            # PyTorch Conv1d (approximate filtering)
            if self.competitors['torch']:
                print("  PyTorch Conv1d...", end=" ", flush=True)
                try:
                    import torch
                    # Create simple filter kernel
                    kernel = torch.tensor([0.25, 0.5, 0.25], dtype=torch.float32).view(1, 1, -1)
                    data_torch = torch.from_numpy(data).float().unsqueeze(0).unsqueeze(0)
                    
                    timer = BenchmarkTimer()
                    for _ in range(self.config.WARMUP_RUNS):
                        _ = torch.nn.functional.conv1d(data_torch, kernel, padding=1)
                    for _ in range(self.config.ITERATIONS):
                        timer.start()
                        _ = torch.nn.functional.conv1d(data_torch, kernel, padding=1)
                        timer.stop()
                    torch_time = timer.mean()
                    results[f"PyTorch_{size}"] = torch_time
                    print(f"✓ {torch_time:.3f}ms")
                except Exception as e:
                    print(f"✗ Error: {str(e)[:30]}")
        
        self.results['filtering'] = results
        return results
    
    def benchmark_matrix_multiplication(self):
        """Benchmark matrix multiplication."""
        print("\n" + "="*70)
        print("TEST 3: MATRIX MULTIPLICATION")
        print("="*70)
        
        results = {}
        
        for size in self.config.MATRIX_SIZES:
            print(f"\n📊 Matrix Size: {size}×{size}")
            print("-" * 70)
            
            # Generate test data
            A = np.random.randn(size, size).astype(np.float64)
            B = np.random.randn(size, size).astype(np.float64)
            
            # BASELINE: NumPy matmul
            print("  NumPy matmul...", end=" ", flush=True)
            timer = BenchmarkTimer()
            for _ in range(self.config.WARMUP_RUNS):
                _ = np.matmul(A, B)
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = np.matmul(A, B)
                timer.stop()
            numpy_time = timer.mean()
            results[f"NumPy_{size}"] = numpy_time
            print(f"✓ {numpy_time:.3f}ms")
            
            # Crystalline Tier 1
            print("  Crystalline Tier 1...", end=" ", flush=True)
            timer = BenchmarkTimer()
            for _ in range(self.config.WARMUP_RUNS):
                _ = self.backend.matrix_multiply(A, B)
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = self.backend.matrix_multiply(A, B)
                timer.stop()
            crystalline_time = timer.mean()
            results[f"Crystalline_{size}"] = crystalline_time
            print(f"✓ {crystalline_time:.3f}ms")
            
            # PyTorch matmul (CPU)
            if self.competitors['torch']:
                print("  PyTorch matmul (CPU)...", end=" ", flush=True)
                try:
                    import torch
                    A_torch = torch.from_numpy(A)
                    B_torch = torch.from_numpy(B)
                    
                    timer = BenchmarkTimer()
                    for _ in range(self.config.WARMUP_RUNS):
                        _ = torch.matmul(A_torch, B_torch)
                    for _ in range(self.config.ITERATIONS):
                        timer.start()
                        _ = torch.matmul(A_torch, B_torch)
                        timer.stop()
                    torch_time = timer.mean()
                    results[f"PyTorch_{size}"] = torch_time
                    print(f"✓ {torch_time:.3f}ms")
                except Exception as e:
                    print(f"✗ Error: {str(e)[:30]}")
            
            # TensorFlow matmul (CPU)
            if self.competitors['tensorflow']:
                print("  TensorFlow matmul (CPU)...", end=" ", flush=True)
                try:
                    import tensorflow as tf
                    A_tf = tf.constant(A)
                    B_tf = tf.constant(B)
                    
                    timer = BenchmarkTimer()
                    for _ in range(self.config.WARMUP_RUNS):
                        _ = tf.matmul(A_tf, B_tf)
                    for _ in range(self.config.ITERATIONS):
                        timer.start()
                        _ = tf.matmul(A_tf, B_tf)
                        timer.stop()
                    tf_time = timer.mean()
                    results[f"TensorFlow_{size}"] = tf_time
                    print(f"✓ {tf_time:.3f}ms")
                except Exception as e:
                    print(f"✗ Error: {str(e)[:30]}")
        
        self.results['matrix_multiplication'] = results
        return results
    
    def benchmark_linear_solve(self):
        """Benchmark linear system solving (Ax=b)."""
        print("\n" + "="*70)
        print("TEST 4: LINEAR SYSTEM SOLVING (Ax=b)")
        print("="*70)
        
        results = {}
        
        for size in self.config.MATRIX_SIZES:
            print(f"\n📊 System Size: {size}×{size}")
            print("-" * 70)
            
            # Generate test data
            A = np.random.randn(size, size).astype(np.float64)
            A = A @ A.T + np.eye(size)  # Make it well-conditioned
            b = np.random.randn(size).astype(np.float64)
            
            # BASELINE: NumPy solve
            print("  NumPy solve...", end=" ", flush=True)
            timer = BenchmarkTimer()
            for _ in range(self.config.WARMUP_RUNS):
                _ = np.linalg.solve(A, b)
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = np.linalg.solve(A, b)
                timer.stop()
            numpy_time = timer.mean()
            results[f"NumPy_{size}"] = numpy_time
            print(f"✓ {numpy_time:.3f}ms")
            
            # Crystalline Tier 1 (SciPy-backed)
            print("  Crystalline Tier 1...", end=" ", flush=True)
            timer = BenchmarkTimer()
            for _ in range(self.config.WARMUP_RUNS):
                _ = self.backend.linear_algebra_solve(A, b)
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = self.backend.linear_algebra_solve(A, b)
                timer.stop()
            crystalline_time = timer.mean()
            results[f"Crystalline_{size}"] = crystalline_time
            print(f"✓ {crystalline_time:.3f}ms")
            
            # SciPy linalg.solve
            print("  SciPy linalg.solve...", end=" ", flush=True)
            timer = BenchmarkTimer()
            for _ in range(self.config.WARMUP_RUNS):
                _ = linalg.solve(A, b)
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = linalg.solve(A, b)
                timer.stop()
            scipy_time = timer.mean()
            results[f"SciPy_{size}"] = scipy_time
            print(f"✓ {scipy_time:.3f}ms")
        
        self.results['linear_solve'] = results
        return results
    
    def benchmark_convolution(self):
        """Benchmark 1D convolution."""
        print("\n" + "="*70)
        print("TEST 5: 1D CONVOLUTION")
        print("="*70)
        
        results = {}
        
        for size in self.config.ARRAY_SIZES:
            print(f"\n📊 Array Size: {size:,} samples, Kernel: 7")
            print("-" * 70)
            
            # Generate test data
            data = np.random.randn(size).astype(np.float64)
            kernel = np.random.randn(7).astype(np.float64)
            
            # BASELINE: SciPy convolve
            print("  SciPy convolve...", end=" ", flush=True)
            timer = BenchmarkTimer()
            for _ in range(self.config.WARMUP_RUNS):
                _ = signal.convolve(data, kernel, mode='same')
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = signal.convolve(data, kernel, mode='same')
                timer.stop()
            scipy_time = timer.mean()
            results[f"SciPy_{size}"] = scipy_time
            print(f"✓ {scipy_time:.3f}ms")
            
            # Crystalline Tier 1
            print("  Crystalline Tier 1...", end=" ", flush=True)
            timer = BenchmarkTimer()
            for _ in range(self.config.WARMUP_RUNS):
                _ = self.backend.convolution(data, kernel, padding=0)
            for _ in range(self.config.ITERATIONS):
                timer.start()
                _ = self.backend.convolution(data, kernel, padding=0)
                timer.stop()
            crystalline_time = timer.mean()
            results[f"Crystalline_{size}"] = crystalline_time
            print(f"✓ {crystalline_time:.3f}ms")
            
            # PyTorch Conv1d
            if self.competitors['torch']:
                print("  PyTorch Conv1d...", end=" ", flush=True)
                try:
                    import torch
                    kernel_torch = torch.from_numpy(kernel).view(1, 1, -1)
                    data_torch = torch.from_numpy(data).unsqueeze(0).unsqueeze(0)
                    
                    timer = BenchmarkTimer()
                    for _ in range(self.config.WARMUP_RUNS):
                        _ = torch.nn.functional.conv1d(data_torch, kernel_torch, padding=3)
                    for _ in range(self.config.ITERATIONS):
                        timer.start()
                        _ = torch.nn.functional.conv1d(data_torch, kernel_torch, padding=3)
                        timer.stop()
                    torch_time = timer.mean()
                    results[f"PyTorch_{size}"] = torch_time
                    print(f"✓ {torch_time:.3f}ms")
                except Exception as e:
                    print(f"✗ Error: {str(e)[:30]}")
        
        self.results['convolution'] = results
        return results
    
    def generate_summary_report(self):
        """Generate summary report of all benchmarks."""
        print("\n" + "="*70)
        print("BENCHMARK SUMMARY REPORT")
        print("="*70)
        
        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "config": {
                "iterations": self.config.ITERATIONS,
                "warmup_runs": self.config.WARMUP_RUNS,
            },
            "tests": {}
        }
        
        for test_name, test_results in self.results.items():
            print(f"\n📊 {test_name.upper().replace('_', ' ')}")
            print("-" * 70)
            
            # Find Crystalline results
            crystalline_results = {k: v for k, v in test_results.items() if 'Crystalline' in k}
            
            if crystalline_results:
                avg_crystalline = np.mean(list(crystalline_results.values()))
                print(f"Average Crystalline Time: {avg_crystalline:.3f}ms")
                
                # Compare with others
                other_results = {k: v for k, v in test_results.items() if 'Crystalline' not in k}
                
                if other_results:
                    print("\nComparison vs Competitors:")
                    for lib_name, lib_time in sorted(other_results.items(), key=lambda x: x[1]):
                        ratio = lib_time / avg_crystalline if avg_crystalline > 0 else 0
                        print(f"  {lib_name:30s} {lib_time:8.3f}ms (ratio: {ratio:.2f}x)")
                
                summary["tests"][test_name] = {
                    "crystalline_avg_ms": float(avg_crystalline),
                    "all_results": {k: float(v) for k, v in test_results.items()}
                }
        
        return summary
    
    def save_results(self, filename="benchmark_results.json"):
        """Save results to JSON file."""
        summary = self.generate_summary_report()
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ Results saved to: {filename}")
        return filename


def main():
    """Run complete benchmark suite."""
    print("\n" + "="*70)
    print("🚀 CRYSTALLINE GPU TIER 1 - BENCHMARK SUITE")
    print("="*70)
    print("\nThis benchmark compares Crystalline GPU Tier 1 (CPU-based)")
    print("against industry-standard libraries:")
    print("  - NumPy (scientific computing baseline)")
    print("  - SciPy (signal processing)")
    print("  - Scikit-learn (machine learning)")
    print("  - PyTorch (deep learning, CPU backend)")
    print("  - TensorFlow (deep learning, CPU backend)")
    print("\n" + "="*70)
    
    # Create benchmark instance
    benchmark = CrystallineBenchmark()
    
    # Import Crystalline
    if not benchmark.import_crystalline():
        print("❌ Cannot run benchmarks without Crystalline GPU")
        return
    
    # Import competitors
    benchmark.import_competitors()
    
    # Run all benchmarks
    try:
        benchmark.benchmark_spectral_analysis()
        benchmark.benchmark_filtering()
        benchmark.benchmark_matrix_multiplication()
        benchmark.benchmark_linear_solve()
        benchmark.benchmark_convolution()
        
        # Generate report
        summary = benchmark.generate_summary_report()
        
        # Save results
        benchmark.save_results("d:\\crystalline-tier1-open\\benchmarks\\benchmark_results.json")
        
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
