# GitHub Repository Guide

This repository is already hosted on GitHub. This document records the current
repository facts and the checks to perform when maintaining or publishing the
Tier 1 package.

## Repository

- Repository: `ficklecreationstudios-boop/crystalline-tier1`
- Default branch: `main`
- Remediation work: `founder-audit-remediation`
- Published scope: CPU-only Tier 1 numerical and signal-processing utilities
- License: GPL-3.0

The GPL-3.0 license governs redistribution and licensing obligations; it does
not by itself require a particular GitHub visibility setting. Repository
visibility and branch protections are separate GitHub configuration choices.

## Current package structure

```text
crystalline-tier1/
├── crystalline/
│   ├── api.py
│   ├── backend.py
│   ├── licensing/
│   └── kernels/
├── docs/
├── benchmarks/
├── tests/
├── audit/
├── README.md
├── REPO_SUMMARY.md
├── CONTRIBUTING.md
├── LICENSE
└── pyproject.toml
```

The repository's source of truth is the actual tree on GitHub. Do not rely on
older setup examples that mention files which are no longer present.

## Development checks

The package declares Python 3.10+ support and depends on NumPy and SciPy.
The development extras include pytest and related tooling.

Before proposing a release or merge:

1. Run the complete pytest suite.
2. Run the repository's configured critical static checks.
3. Verify package metadata and a clean build/install path.
4. Treat benchmark results as evidence for the exact environment and workload
   measured; do not convert a local timing into a universal performance claim.
5. Keep GPU and higher-tier functionality described as unavailable unless a
   corresponding implementation and independent evidence have been added.

## GitHub Actions

The repository has a GitHub Actions test workflow covering the supported Python
versions and operating systems configured by the project. A green workflow is
evidence for the tested revision only; it is not a claim of production
readiness or universal platform compatibility.

## Branch protection

Branch protection, required reviews, required status checks, and automatic
branch deletion are GitHub repository settings. They should be verified in the
repository settings rather than described as enabled merely because a setup
guide recommends them.

## Publishing

Package publishing is a separate release action. Building a wheel or source
distribution does not mean the package has been published to PyPI.

For a release, verify the version in `pyproject.toml`, build artifacts in a
clean environment, inspect the generated metadata, run installation/import
smoke tests, and only then publish through the project's chosen distribution
channel.

## Evidence standard

Claims about correctness, performance, security, licensing, or production
readiness must be supported by the corresponding implementation and evidence.
If evidence is unavailable, narrow the claim rather than filling the gap with
historical benchmark output or configuration recommendations.
