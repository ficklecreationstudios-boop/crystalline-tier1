# Crystalline Tier 1 — Repository Summary

## Current scope

This repository contains the free Tier 1 edition of Crystalline: a CPU-only Python numerical and signal-processing utility package built on NumPy and SciPy.

### Implemented capabilities

- One-dimensional spectral analysis with one-sided density-scaled PSD output.
- Butterworth filtering through SciPy's digital filter routines.
- CPU matrix multiplication.
- CPU linear-system solving.
- One-dimensional convolution with optional zero padding and stride.
- Source-visible experimental spectral helpers.
- Tier 1 runtime enforcement that blocks GPU and higher-tier features.

### Explicitly unavailable

- GPU execution.
- JIT-specialized execution as a Tier 1 feature.
- Domain-specific wheels.
- Commercial or enterprise support/licensing features.

## Audit status

The repository underwent a founder-level audit because its historical benchmark reports made broader performance claims than the evidence supported. The frozen production boundary is preserved on `main` at commit `fa7ad15be712032500d29d161099923e24089080`.

Remediation is being developed on `founder-audit-remediation` and must not be interpreted as a change to the frozen `main` boundary until deliberately merged.

## Numerical validation

Independent tests compare core behavior with NumPy/SciPy reference implementations. Current coverage includes:

- even- and odd-length PSD calculations;
- sampling-rate validation;
- normalized Butterworth filtering;
- convolution stride behavior;
- experimental spectral helper equivalence;
- invalid FFT input handling.

## Performance evidence

Historical benchmark artifacts are retained for provenance but are quarantined from current product claims. A replacement benchmark compares equivalent mathematical operations and records environment-specific timing statistics. It does not create a blanket speed-up claim.

The project follows this evidence order:

1. Numerical correctness.
2. Reproducible methodology.
3. Performance measurement.
4. Product positioning.

## Packaging

The project uses `pyproject.toml`, supports Python 3.10+, and declares NumPy and SciPy as runtime dependencies. CI tests Python 3.10–3.12 on Ubuntu, Windows, and macOS.

## Support

Bug reports and project discussion belong in the repository's GitHub Issues. No sales contact or higher-tier pricing is asserted by this Tier 1 repository.

## Important interpretation

This document is a current repository summary, not a performance advertisement. Statements about speed, production readiness, GPU acceleration, or future tiers require separate evidence and are not inferred from the existence of this package.
