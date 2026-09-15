# Crystalline Tier 1 — Benchmark Archive

This directory contains historical benchmark scripts and outputs from the pre-remediation repository state. They are retained for auditability and reproducibility work, not as current marketing or performance evidence.

## Historical benchmark scope

The original suite exercised:

- spectral analysis;
- Butterworth filtering;
- dense matrix multiplication;
- linear-system solving; and
- one-dimensional convolution.

It compared the CPU implementation with selected NumPy, SciPy, and PyTorch CPU paths. The exact historical environment and semantics varied between benchmark generations, which is why the resulting reports are now treated as archival observations.

## Running the archived scripts

The scripts remain available for forensic reproduction, but rerunning them should not be described as a current benchmark unless the run records the exact commit, dependencies, hardware, operating system, thread settings, input generation, warm-up policy, repetitions, and raw observations.

```bash
python quick_benchmark.py
python comprehensive_benchmark.py
python report_generator.py
```

## Current benchmark policy

A replacement benchmark is gated on numerical correctness. The new benchmark must use identical mathematical semantics across implementations and must distinguish cold-start from steady-state performance.

The project currently makes **no universal performance claim**, including no fixed speed-up percentage, no claim of production readiness based on timing tables alone, and no forecast of future GPU-tier acceleration.

For the historical evidence-bounded record, see `BENCHMARK_REPORT.md` and `BENCHMARK_SUMMARY.md`.
