# Founder Audit — Claim Disposition

## Frozen production boundary

The audit began from `main` commit `fa7ad15be712032500d29d161099923e24089080`, tree `933dda3c5784a23d993ccf13e37674ae9a2278c1`. That boundary remains unchanged on `main`.

## Current claim standard

Every public claim must be one of:

- **Implemented:** directly supported by the current source and tests.
- **Reference-aligned:** numerical behavior is checked against an independent NumPy/SciPy reference.
- **Benchmark-specific:** supported only for a named operation, environment, and methodology.
- **Unavailable:** explicitly outside Tier 1 scope.
- **Historical:** retained for provenance but not presented as a current capability.
- **Intended architecture:** a product-tier requirement that is not evidence of implementation in this Tier 1 repository.

## Dispositions

| Claim | Finding | Action |
|---|---|---|
| Tier 1 is CPU-only | Supported | Retained and made explicit. |
| Spectral analysis provides a one-sided density-scaled PSD | Supported after numerical correction | Backend implementation and independent even/odd-length tests aligned to SciPy periodogram semantics. |
| Convolution supports stride | Previously incomplete | Implemented stride validation and output selection; independent test added. |
| Filtering accepts physical Hz cutoffs | Unsupported by the API | Corrected documentation/examples to normalized SciPy cutoffs because no sampling-frequency parameter exists. |
| Experimental spectral helper is a faster optimized path | Unsupported | Removed performance positioning; kept it source-visible and correctness-aligned. |
| Tier 1 is universally faster / 10x faster / within 10–20% | Unsupported | Removed from current public positioning; historical artifacts quarantined. |
| Tier 1 has GPU execution | False for this distribution | Explicitly unavailable. `GPUBackend` is a blocking placeholder; `get_backend()` and `set_backend()` dispatch only to the CPU backend. |
| Tier 4 is intended to unlock GPU + JIT + Champion Mode | Intended architecture | This is a product-tier requirement, not a Tier 1 implementation claim. The current Tier 1 repository does not contain the Tier 4 runtime. |
| Current repository implements Tier 4 | Unsupported | No Tier 4 runtime, backend, or tier-specific executable package was found in the remediation tree. Do not imply Tier 4 is shipped by this repository. |
| Historical frozen code contained optional Numba JIT | Historical / partially implemented | The frozen `fa7ad15` spectral helper imported optional Numba and defined JIT window kernels, but the public backend did not expose a Tier 4 runtime and the helper had incorrect/unsupported performance semantics. The remediation branch removed this dead optional path rather than treating it as Tier 4 evidence. |
| Repository contains a Numba CUDA/JIT execution path today | False | No current Tier 1 Numba import, dependency, JIT decorator, CUDA kernel, or dispatch path was found. Requirements state this explicitly. |
| Repository contains a CuPy execution path | False | No current Tier 1 CuPy dependency, import, backend, or dispatch path was found. |
| PyTorch provides a Crystalline GPU execution path | False | PyTorch appears only as an optional benchmark comparator. The current reproducible benchmark uses CPU PyTorch operations when installed and does not dispatch Crystalline operations through PyTorch or CUDA. |
| Historical benchmark scripts prove GPU execution | False | Historical scripts benchmark CPU implementations/comparators; archive status is retained and GPU conclusions remain quarantined. |
| Higher-tier prices/performance targets are established by this repository | Unsupported | Removed from Tier 1 documentation. |
| Production readiness is established by historical timings | Unsupported | Removed. |
| Package metadata can drift between `setup.py` and `pyproject.toml` | Prevented | `setup.py` is now a metadata-free compatibility shim; `pyproject.toml` is the single metadata source. |
| Installed package contains repository-only test/docs/example artifacts | Prevented and CI-checked | Explicit setuptools discovery excludes those directories; CI builds and installs the wheel into an isolated environment and verifies the installed boundary. |
| Public examples reflect the current API | Verified after correction | Examples were audited; the spectral example handles optional plotting correctly and displays the full PSD range; the linear-algebra example no longer advertises an unsupported higher-tier upgrade. All four examples have CI smoke coverage, including Windows console execution. |
| Reproducible spectral performance advantage exists | Benchmark-specific | Latest green CI run `34987294718` measured Crystalline median times of 0.046 ms, 0.214 ms, and 3.709 ms for 1,024, 10,240, and 102,400 samples versus 0.198 ms, 1.005 ms, and 11.944 ms for equivalent SciPy periodogram semantics. |
| Matrix multiplication is independently accelerated | Unsupported | Latest CI benchmark measured approximately parity with NumPy at 256² and 1024²; no acceleration claim is made. |

## GPU/CUDA/accelerator trace

The remediation branch was traced across its repository tree and executable source/benchmark paths. The current architecture is CPU-only:

1. `crystalline.backend.CPUBackend` implements every available Tier 1 operation with NumPy/SciPy.
2. `crystalline.backend.GPUBackend` is a deliberate blocking placeholder that raises `TierFeatureBlockedError` on construction.
3. `get_backend()` always returns `CPUBackend`; `set_backend()` rejects every backend name other than `cpu`.
4. `crystalline.licensing.TIER_FEATURES` explicitly marks `gpu_acceleration`, `champion_mode`, and `jit_compilation` false for Tier 1.
5. `crystalline.get_tier_info()` reports `gpu_available=False` and `jit_available=False`.
6. `crystalline/kernels/` is a CPU kernel inventory; its unavailable inventory explicitly lists GPU operations as not implemented.
7. `crystalline/kernels/spectral.py` contains NumPy/SciPy CPU helpers only. There is no current Numba decorator, CUDA kernel, CuPy array path, PyTorch dispatch, or device-selection logic.
8. `requirements.txt` contains only NumPy/SciPy runtime dependencies; it explicitly states that Numba is not used by the current implementation.
9. PyTorch is imported only conditionally by the reproducible benchmark as an external comparator. Its current benchmark uses CPU tensors and explicitly omits raw PyTorch FFT as a non-equivalent PSD comparison.
10. Historical frozen commit `fa7ad15` did contain optional CPU Numba JIT window helpers, but those helpers were not a GPU backend, were not wired as a Tier 4 runtime, and did not establish a GPU execution claim. The frozen commit's own message also described the work as Tier 1 optimization.
11. The repository's initial release commit described itself as “Crystalline GPU Tier 1,” but its backend still explicitly blocked GPU execution. That name is therefore historical branding, not evidence of a shipped GPU runtime.

### Correct architectural interpretation

The intended product architecture can legitimately reserve GPU, JIT specialization, and Champion Mode for Tier 4. Tier 1 should therefore remain CPU-only and should reject those features. The audit must not collapse the intended Tier 4 contract into the Tier 1 implementation question.

The remaining Tier 4 question is separate: **where is the Tier 4 implementation, and does it actually exist anywhere in the product/repository lineage?** This Tier 1 repository does not answer that question. A Tier 4 claim requires the corresponding implementation or a separate Tier 4 repository/package to be identified and independently tested.

A real Tier 4 E2E program would require, at minimum, a real accelerator backend, explicit device dispatch, JIT compilation behavior, Champion Mode semantics, CPU/GPU numerical parity tests, dependency/toolchain policy, GPU-capable CI/test infrastructure, and independent GPU/JIT performance benchmarks. Numba's current CUDA architecture is one possible implementation route, but it requires an NVIDIA CUDA environment and current `numba-cuda` tooling; it should not be assumed to be the intended implementation without evidence. citeturn0search0turn0search1

## Benchmark gate

The replacement benchmark compares equivalent mathematical operations. Raw FFT timings are not used as evidence for a PSD API because they omit windowing and PSD density normalization.

The latest reproducible CI benchmark completed successfully only after the full 3-OS × 3-Python correctness matrix passed. Run `34987294718` also completed the isolated wheel/sdist packaging checks and benchmark. Its benchmark artifact is retained by GitHub Actions for provenance. The artifact digest is `sha256:0c792847d30717bfab19e7f3b50e88e959597be74c085ba4133fc3b69bd72096`. The benchmark is evidence for the tested CI environment and workloads only; it does not establish universal acceleration.

## Remediation principle

When a claim fails because the implementation is weaker than the intended contract but the contract itself is reasonable, repair the implementation and add an independent regression test. When the claim is unsupported by the available evidence, narrow or remove the claim rather than altering code solely to make a benchmark look favorable.
