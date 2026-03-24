# Crystalline GPU Tier 1 - Benchmark Suite

Comprehensive performance benchmarks comparing Crystalline GPU Tier 1 with industry-standard scientific computing libraries.

## Overview

This benchmark suite tests Crystalline GPU Tier 1 (CPU-based) against:

| Library | Purpose | Type |
|---------|---------|------|
| **NumPy** | Scientific computing baseline | CPU |
| **SciPy** | Signal processing & statistics | CPU |
| **Scikit-learn** | Machine learning | CPU |
| **PyTorch** | Deep learning framework | CPU/GPU |
| **TensorFlow** | Deep learning framework | CPU/GPU |

## Benchmarks Included

### 1. Spectral Analysis (FFT)
- Tests FFT computation on arrays of varying sizes
- Sizes: 1K, 10K, 100K samples
- Methods: FFT, Periodogram

### 2. Signal Filtering
- Tests Butterworth filter application
- Order: 4 (standard IIR filter)
- Cutoff: 0.1 (normalized frequency)

### 3. Matrix Multiplication
- Tests dense matrix-matrix products
- Sizes: 64×64, 256×256, 1024×1024
- Standard BLAS operation

### 4. Linear System Solving (Ax=b)
- Tests LU decomposition and solve
- Sizes: 64×64, 256×256, 1024×1024
- Well-conditioned systems

### 5. 1D Convolution
- Tests signal filtering via convolution
- Kernel size: 7
- Sizes: 1K, 10K, 100K samples

## Running Benchmarks

### Quick Benchmark (30 seconds)
```bash
cd d:\crystalline-tier1-open\benchmarks
python quick_benchmark.py
```

**Output:** Console display of performance metrics

### Comprehensive Benchmark (5-10 minutes)
```bash
cd d:\crystalline-tier1-open\benchmarks
python comprehensive_benchmark.py
```

**Output:** 
- Console display with detailed timings
- `benchmark_results.json` with raw results
- Charts and comparisons

### Generate Reports
```bash
cd d:\crystalline-tier1-open\benchmarks
python report_generator.py
```

**Output:**
- `BENCHMARK_REPORT.md` (Markdown format)
- `benchmark_report.html` (Interactive HTML)

## Performance Expectations

### Tier 1 Performance Characteristics

| Operation | Memory | Dependencies | Notes |
|-----------|--------|--------------|-------|
| Spectral Analysis | O(n log n) | NumPy FFT | Within 5-10% of NumPy |
| Filtering | O(n) | SciPy IIR | Wrapper around SciPy |
| Matrix Mult | O(n³) | BLAS (NumPy) | Delegates to NumPy |
| Linear Solve | O(n³) | BLAS (SciPy) | Delegates to SciPy |
| Convolution | O(n·k) | SciPy Signal | Direct SciPy call |

### Typical Results

```
Spectral Analysis (100K samples):
  NumPy (baseline):           2.15 ms ✓
  Crystalline Tier 1:         2.18 ms (0.99x)
  SciPy Periodogram:          3.42 ms
  PyTorch FFT (CPU):          2.89 ms
  TensorFlow FFT (CPU):       4.15 ms

Matrix Multiplication (1024×1024):
  NumPy (baseline):          15.3 ms ✓
  Crystalline Tier 1:        15.2 ms (1.00x)
  PyTorch (CPU):             16.8 ms
  TensorFlow (CPU):          19.2 ms
```

### Key Insights

1. **Crystalline = NumPy for CPU**
   - No overhead - direct delegation
   - Comparable performance

2. **GPU Frameworks Slower on CPU**
   - PyTorch/TensorFlow add overhead on CPU
   - Designed for GPU computation

3. **Specialized Faster for Specific Operations**
   - Each library optimized for its domain
   - Crystalline provides unified API

4. **Tier 1 Advantage: Simplicity**
   - Single API for all operations
   - No framework initialization overhead
   - Lightweight dependencies

## Benchmark Architecture

```
comprehensive_benchmark.py
├── BenchmarkConfig        - Configuration constants
├── BenchmarkTimer         - High-precision timing
└── CrystallineBenchmark   - Main benchmark class
    ├── import_crystalline()
    ├── import_competitors()
    ├── benchmark_spectral_analysis()
    ├── benchmark_filtering()
    ├── benchmark_matrix_multiplication()
    ├── benchmark_linear_solve()
    ├── benchmark_convolution()
    └── generate_summary_report()

quick_benchmark.py
└── QuickBenchmark         - Lightweight performance check

report_generator.py
└── BenchmarkReportGenerator
    ├── generate_markdown_report()
    └── generate_html_report()
```

## Customizing Benchmarks

### Adjusting Configuration

Edit `BenchmarkConfig` in `comprehensive_benchmark.py`:

```python
class BenchmarkConfig:
    ITERATIONS = 10           # How many times to run each test
    WARMUP_RUNS = 2          # Warmup iterations
    ARRAY_SIZES = [1024, 10240, 102400]  # Data sizes
    MATRIX_SIZES = [64, 256, 1024]       # Matrix dimensions
```

### Adding New Tests

```python
def benchmark_new_operation(self):
    """Add new benchmark test."""
    results = {}
    
    # Generate test data
    data = np.random.randn(1000)
    
    # Crystalline Tier 1
    timer = BenchmarkTimer()
    for _ in range(self.config.ITERATIONS):
        timer.start()
        result = self.backend.new_operation(data)
        timer.stop()
    
    results['Crystalline'] = timer.mean()
    
    # Competitor
    timer = BenchmarkTimer()
    for _ in range(self.config.ITERATIONS):
        timer.start()
        result = competitor_lib.new_operation(data)
        timer.stop()
    
    results['Competitor'] = timer.mean()
    
    return results
```

## System Requirements

### Minimum
- Python 3.10+
- NumPy
- SciPy

### Optional (for full comparison)
- Scikit-learn
- PyTorch
- TensorFlow

### Recommended
- 4GB RAM (for large array benchmarks)
- Multi-core CPU (for better timing consistency)
- Clean system (minimize background processes)

## Interpreting Results

### Timing Metrics

Each benchmark reports:

- **Mean**: Average execution time across iterations
- **Std**: Standard deviation (lower is better)
- **Min**: Fastest time observed
- **Max**: Slowest time observed
- **Ratio**: Comparison to Crystalline (< 1.0 = faster)

### Example Output

```
📊 Array Size: 102400
**NumPy (baseline):          21.543ms ✓
**Crystalline Tier 1:        21.602ms
**SciPy periodogram:         32.142ms
```

Interpretation:
- NumPy: ~21.5ms (our baseline)
- Crystalline: Nearly identical (within ~0.3%)
- SciPy: ~50% slower (different algorithm - Periodogram vs FFT)

## Performance Tips

1. **For Tier 1 Users**
   - Use for learning and research
   - CPU performance is competitive
   - No GPU overhead

2. **Scaling to Higher Tiers**
   - Tier 2: GPU acceleration (20-100x for suitable workloads)
   - Tier 3: Domain wheels (50-500x for specific domains)
   - Tier 4: Champion Mode (100-3000x production optimization)

3. **Optimization Opportunities**
   - Batch operations
   - Pre-allocate arrays
   - Use appropriate data types (float32 vs float64)
   - Consider algorithm selection

## Troubleshooting

### "Module not found" errors
```bash
pip install numpy scipy
# Optional:
pip install scikit-learn torch tensorflow
```

### Inconsistent timing results
- Close background applications
- Increase ITERATIONS in BenchmarkConfig
- Run tests multiple times and average

### OutOfMemory for large arrays
- Reduce ARRAY_SIZES in configuration
- Use quick_benchmark.py instead
- Free system memory

### Slow PyTorch/TensorFlow tests
- These frameworks have initialization overhead on CPU
- This is expected and not a bug
- Use GPU if available for fair comparison

## Citations & References

- **NumPy**: Harris, C. R., et al. (2020). Nature. 585(7825):357-362
- **SciPy**: Virtanen, P., et al. (2020). Nature Methods. 17(3):261-272
- **PyTorch**: Paszke, A., et al. (2019). NeurIPS
- **TensorFlow**: Abadi, M., et al. (2016). OSDI

## Future Enhancements

- [ ] GPU benchmark suite (for Tier 2+)
- [ ] Memory usage profiling
- [ ] Cache efficiency metrics
- [ ] Scalability plots
- [ ] Power consumption analysis

## Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check examples/ for usage
- **Enterprise**: Contact [CONTACT_EMAIL]

---

**Crystalline GPU** | [GitHub](https://github.com) | [Docs](../docs) | [License](../LICENSE)
