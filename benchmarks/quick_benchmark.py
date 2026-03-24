"""
Quick Benchmark Suite - Fast Tier 1 Performance Check

Run this for a quick performance baseline without competitors
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import numpy as np
from crystalline import get_backend, spectral_analysis, spectral_filtering


class QuickBenchmark:
    """Quick benchmark without competitors."""
    
    def __init__(self):
        self.backend = get_backend()
        self.results = {}
    
    def time_operation(self, func, *args, **kwargs):
        """Time a single operation."""
        # Warmup
        func(*args, **kwargs)
        
        # Measure
        times = []
        for _ in range(10):
            start = time.perf_counter()
            func(*args, **kwargs)
            times.append((time.perf_counter() - start) * 1000)
        
        return {
            "mean_ms": np.mean(times),
            "std_ms": np.std(times),
            "min_ms": np.min(times),
            "max_ms": np.max(times)
        }
    
    def benchmark_tier1(self):
        """Benchmark Tier 1 operations."""
        print("\n" + "="*60)
        print("⚡ CRYSTALLINE GPU TIER 1 - QUICK BENCHMARK")
        print("="*60)
        
        # Test 1: Spectral Analysis
        print("\n1️⃣  Spectral Analysis (1M samples)")
        data = np.random.randn(1_000_000)
        result = self.time_operation(spectral_analysis, data, fs=100.0)
        print(f"   Mean:   {result['mean_ms']:.3f} ms")
        print(f"   Std:    {result['std_ms']:.3f} ms")
        print(f"   Range:  {result['min_ms']:.3f} - {result['max_ms']:.3f} ms")
        self.results['spectral_analysis'] = result
        
        # Test 2: Filtering
        print("\n2️⃣  Spectral Filtering (1M samples)")
        data = np.random.randn(1_000_000)
        result = self.time_operation(spectral_filtering, data, cutoff=0.1, order=4)
        print(f"   Mean:   {result['mean_ms']:.3f} ms")
        print(f"   Std:    {result['std_ms']:.3f} ms")
        print(f"   Range:  {result['min_ms']:.3f} - {result['max_ms']:.3f} ms")
        self.results['filtering'] = result
        
        # Test 3: Matrix Multiplication
        print("\n3️⃣  Matrix Multiplication (1024×1024)")
        A = np.random.randn(1024, 1024)
        B = np.random.randn(1024, 1024)
        result = self.time_operation(self.backend.matrix_multiply, A, B)
        print(f"   Mean:   {result['mean_ms']:.3f} ms")
        print(f"   Std:    {result['std_ms']:.3f} ms")
        print(f"   Range:  {result['min_ms']:.3f} - {result['max_ms']:.3f} ms")
        self.results['matrix_multiply'] = result
        
        # Test 4: Linear Solve
        print("\n4️⃣  Linear System Solve (1024×1024)")
        A = np.random.randn(1024, 1024)
        A = A @ A.T + np.eye(1024)
        b = np.random.randn(1024)
        result = self.time_operation(self.backend.linear_algebra_solve, A, b)
        print(f"   Mean:   {result['mean_ms']:.3f} ms")
        print(f"   Std:    {result['std_ms']:.3f} ms")
        print(f"   Range:  {result['min_ms']:.3f} - {result['max_ms']:.3f} ms")
        self.results['linear_solve'] = result
        
        print("\n" + "="*60)
        print("✅ Quick benchmark completed!")
        print("="*60)
        
        return self.results


if __name__ == "__main__":
    try:
        benchmark = QuickBenchmark()
        benchmark.benchmark_tier1()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
