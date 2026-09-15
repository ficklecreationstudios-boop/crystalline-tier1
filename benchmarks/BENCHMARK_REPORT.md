# Crystalline Tier 1 — Historical Benchmark Record

**Artifact date:** 2026-03-24  
**Status:** Historical / audit artifact — not a current performance claim

## Purpose

This file preserves benchmark output from the frozen pre-remediation repository state. It is retained for auditability, but its measurements should not be interpreted as evidence that the current implementation is faster than NumPy, SciPy, PyTorch, or any other library.

The founder's audit found that benchmark artifacts were inconsistent with one another and that the repository's broad performance conclusions were not adequately supported. In particular, the old report mixed different benchmark generations and used language such as "within 10–20%" that was not justified across the reported operations and array sizes.

## Frozen results retained for provenance

The original benchmark tables remain below as historical observations. They are **not** reproduced as current capabilities.

### Spectral Analysis

| Library | 1024 | 10240 | 102400 |
|---|---:|---:|---:|
| Crystalline | 0.345 ms | 1.321 ms | 15.299 ms |
| NumPy | 0.019 ms | 0.146 ms | 4.997 ms |
| PyTorch | 0.026 ms | 0.142 ms | 0.585 ms |
| SciPy | 0.282 ms | 1.410 ms | 11.314 ms |

### Filtering

| Library | 1024 | 10240 | 102400 |
|---|---:|---:|---:|
| Crystalline | 0.509 ms | 0.726 ms | 2.277 ms |
| PyTorch | 0.018 ms | 0.047 ms | 0.291 ms |
| SciPy | 0.142 ms | 0.244 ms | 2.169 ms |

### Matrix Multiplication

| Library | 64 | 256 | 1024 |
|---|---:|---:|---:|
| Crystalline | 0.033 ms | 0.411 ms | 14.478 ms |
| NumPy | 0.016 ms | 0.392 ms | 16.138 ms |
| PyTorch | 0.011 ms | 0.232 ms | 14.121 ms |

### Linear Solve

| Library | 64 | 256 | 1024 |
|---|---:|---:|---:|
| Crystalline | 0.137 ms | 1.458 ms | 27.684 ms |
| NumPy | 0.035 ms | 69.509 ms | 215.777 ms |
| SciPy | 0.127 ms | 1.446 ms | 24.346 ms |

### Convolution

| Library | 1024 | 10240 | 102400 |
|---|---:|---:|---:|
| Crystalline | 0.025 ms | 0.061 ms | 0.264 ms |
| PyTorch | 0.020 ms | 0.035 ms | 0.199 ms |
| SciPy | 0.024 ms | 0.059 ms | 0.315 ms |

## What can and cannot be concluded

### Supported by this historical record

- The Tier 1 implementation delegates core numerical work to NumPy/SciPy.
- The measured timings vary substantially by operation, input size, library, and environment.
- Some individual comparisons were close in the recorded environment.

### Not supported

- A universal speed-up factor.
- A blanket claim that Crystalline is within 10–20% of specialized libraries.
- A claim of GPU acceleration in Tier 1.
- A claim that historical timings establish production suitability.
- Forecasts such as 10–100x or 100–3000x improvements for future tiers.

## Reproducibility requirements for a replacement benchmark

A new performance report should be generated only after numerical correctness is independently validated. It should record at minimum:

1. Exact git commit and working-tree state.
2. Python, NumPy, SciPy, and benchmark-script versions.
3. CPU model, OS, BLAS/LAPACK implementation, and thread settings.
4. Identical mathematical semantics across implementations.
5. Warm-up policy, repetition count, timer, and summary statistics.
6. Raw observations rather than only aggregate averages.
7. Separate cold-start and steady-state measurements.
8. Explicit treatment of statistical uncertainty.

Until such a benchmark is produced, performance claims should remain operation- and environment-specific.

---

**Historical artifact preserved during founder-audit remediation.**
