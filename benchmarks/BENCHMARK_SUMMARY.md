# Crystalline Tier 1 — Benchmark Summary

**Status:** Historical / quarantined during founder-audit remediation  
**Original artifact date:** March 24, 2026

## Summary

The repository's original benchmark summary mixed multiple benchmark generations and environments and made conclusions broader than the evidence supported. It is therefore retained only as historical context. It does **not** establish a current speed ranking, a universal acceleration factor, production readiness, or any GPU capability.

The replacement standard is:

> **Correctness first, reproducibility second, performance claims third.**

Numerical behavior must be validated against independent references before timing results are used for product claims.

## Historical observations

The frozen benchmark generation reported approximate Crystalline timings of:

| Operation | Representative recorded size | Historical time |
|---|---:|---:|
| Spectral analysis | 102,400 samples | 15.299 ms |
| Filtering | 102,400 samples | 2.277 ms |
| Matrix multiplication | 1024 × 1024 | 14.478 ms |
| Linear solve | 1024 × 1024 | 27.684 ms |
| Convolution | 102,400 samples | 0.264 ms |

These numbers are observations from the old artifact, not guarantees for the repaired implementation or other machines.

## Removed conclusions

The following types of claims are intentionally no longer presented as facts:

- "10–100x" or similar blanket speed-up claims.
- "100–3000x" future performance claims.
- "within 10–20%" across specialized libraries.
- "production-ready" based solely on the old timing tables.
- Any implication that Tier 1 executes on a GPU.

## Next benchmark gate

A new benchmark should be created only after the numerical correctness suite passes. The benchmark should pin the exact commit, dependency versions, hardware/software environment, thread settings, input generation, warm-up policy, repetitions, and raw timing observations.

Until that gate is met, the project makes no broad performance claim.
