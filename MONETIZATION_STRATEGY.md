# Repository Monetization & Tier Protection Strategy

## Overview

This document explains the architecture and enforcement mechanisms that protect higher-tier monetization while keeping Tier 1 free and open-source.

## Tier Structure

```
Tier 1 (FREE)          Tier 2 (GPU)         Tier 3 (Domain)      Tier 4 (Premium)
├─ CPU-only            ├─ GPU Accel         ├─ Domain Wheels      ├─ Champion Mode
├─ Open Source         ├─ Commercial        ├─ Enterprise         ├─ JIT Compile
├─ GPL-3.0             ├─ $500/mo           ├─ $100K+/yr          ├─ $300K+/yr
└─ No Licensing        └─ Hardware-bound    └─ Support            └─ Support
```

## Monetization Protection Mechanisms

### 1. Feature Blocking (Runtime)

**Location:** `crystalline/licensing/__init__.py`

```python
TIER_FEATURES = {
    "TIER_1_FREE": {
        "gpu_acceleration": False,         # ❌ Blocked
        "champion_mode": False,            # ❌ Blocked
        "jit_compilation": False,          # ❌ Blocked
        "spectral_analysis": True,         # ✅ Allowed
    }
}
```

**Enforcement:** Every high-tier feature call triggers `check_tier_access()` which raises `TierFeatureBlockedError`.

### 2. Architectural Isolation

**GPU Backend Unavailable:**
```python
# crystalline/backend.py
class GPUBackend:
    def __init__(self):
        raise TierFeatureBlockedError(
            "GPU acceleration requires Tier 2+. "
            "Contact sales@crystalline.io"
        )
```

Cannot be instantiated even by accident. Code cannot be bypassed because:
- ✅ Raises exception immediately
- ✅ No fallback or workaround
- ✅ Clear error message with upsell

### 3. Source Code Protection

**File Exclusions (`.gitignore`):**
```
*tier2*
*tier3*
*tier4*
*champion*
*jit_compiler*
crystalline_proprietary/
crystalline_native/
*.cu
*.cuh
```

**Result:** Even if someone forks the repo, they can't access:
- Higher tier wheels
- GPU code (C++/CUDA)
- Proprietary optimizations
- JIT compiler
- Domain wheels

### 4. License Compliance

- ✅ GPL-3.0 for Tier 1 (open-source requirement)
- ✅ License header in all files
- ✅ No license validation (vs full distribution)
- ✅ Clear tier messaging on import

### 5. Dependency Isolation

**Tier 1 Requirements:**
```
numpy>=1.19.0
scipy>=1.5.0
requests>=2.25.0  # For version checking, not GPU licensing
```

**NOT included (Tier 2+):**
- `torch` with CUDA
- `pycuda` / `rocm`
- GPU-specific libraries
- Licensing libraries

### 6. Build System Separation

`setup.py` configured to explicitly exclude higher tiers:

```python
packages=find_packages(exclude=[
    "tests", 
    "docs", 
    "benchmarks",
    # Higher tier packages NOT included
])
```

## Preventing Unauthorized Upgrades

### Scenario 1: User tries to copy files from higher tier

**Protection:**
- .gitignore prevents adding tier 2+ files
- File names explicitly mention tier ("tier2", "tier3", etc.)
- Runtime checks verify tier at import
- Clear error: "This feature requires Tier 2+"

### Scenario 2: User tries to modify licensing module

**Protection:**
- Tier enforcement is in TWO places:
  1. Runtime feature checks
  2. Backend class implementation
- Both must be modified to bypass
- Changes would be obvious in code review
  
### Scenario 3: User tries to reverse-engineer features

**Protection:**
- GPU operations aren't stubbed - they're completely absent
- Linear algebra uses SciPy, not GPU kernels
- No GPU code visible even in files
- Nothing to reverse-engineer

## Commercial Upsell Strategy

### Clear Messaging Throughout

1. **On Import:**
   ```
   WARNING: Crystalline-tier1 is Tier 1 (CPU-only). 
   For GPU acceleration, see https://crystalline.io/tiers
   ```

2. **On Feature Access:**
   ```
   TierFeatureBlockedError: GPU acceleration requires Tier 2+ ($500/month)
   Contact sales@crystalline.io
   ```

3. **In Documentation:**
   - Tier comparison table
   - Feature matrix
   - Contact information for sales
   - Clear upsell language

4. **In Examples:**
   Example 4 specifically shows tier restrictions and upsell

## Verification Checklist

Use this to verify protections are in place:

- [ ] Can't import GPU backend (raises immediately)
- [ ] Can't access "champion_mode" feature (TierFeatureBlockedError)
- [ ] Can't access "jit_compiler" (TierFeatureBlockedError)
- [ ] Tier 2+ wheel files excluded from .gitignore
- [ ] setup.py excludes higher-tier packages
- [ ] License file is GPL-3.0 only
- [ ] License validation disabled
- [ ] All error messages include sales contact info
- [ ] Examples show tier restrictions clearly
- [ ] Tests verify tier enforcement works

## Future Tier Wheels

When publishing Tier 2+:

```
crystalline-tier1           # This repo - Free
crystalline-tier2-cuda      # Separate repo - Commercial
crystalline-tier2-rocm      # Separate repo - Commercial
crystalline-tier3-domains   # Separate repo - Enterprise
crystalline-tier4-champion  # Separate repo - Premium
```

Each is a SEPARATE package with:
- Own repository
- Own commercial license
- Own licensing system
- Own authentication

## Revenue Stream

```
Tier 1 - Free ($0)
├─ Acquisition funnel
├─ Community building
├─ Bug reports/feedback
└─ Marketing demo

Tier 2 - GPU ($500/mo)
├─ Individual researchers/developers
├─ ~$6,000/year per customer
└─ Target: 50-100 customers = $300K-$600K/year

Tier 3 - Domain ($100K+/year)
├─ Large research institutions
├─ Pharma, Finance, Energy companies
└─ Target: 5-10 customers = $500K-$1M/year

Tier 4 - Premium ($300K+/year)
├─ Enterprise clients
├─ Production systems
├─ Dedicated support
└─ Target: 2-5 customers = $600K-$1.5M/year

TOTAL POTENTIAL: $1.4M-$3.1M/year
```

## Security Audit

Anyone reviewing this code should verify:

1. **No GPU code in Tier 1** - Only CPU/NumPy/SciPy
2. **No Licensing system in Tier 1** - Validation disabled
3. **No Commercial code in Tier 1** - GPL-3.0 compliant
4. **All blocks are enforce at multiple levels** - Defense in depth
5. **Clear error messages** - Include sales info, don't hide them

## Q&A

**Q: Can't someone just bypass the tier checks?**
A: They could modify the code if they fork, but:
- Changes are obvious in code review
- They can't access higher-tier features (not in repo)
- They get GPL-3.0 obligation to release modifications
- No business value to them (CPU software is commodity)

**Q: What about licensing bypass?**
A: Tier 1 has NO licensing system - it's open-source GPL-3.0. No bypass needed because there's nothing to bypass.

**Q: Won't PyPI have the full codebase?**
A: No - PyPI gets what's in THIS repo (Tier 1 only) via `setup.py`.
Higher tiers are separate packages on separate repositories.

**Q: What if someone forks and sells it?**
A: GPL-3.0 requires them to:
- Release source code
- Include license
- Credit original authors
- They're legally obligated to keep it free/open

## Conclusion

This Tier 1 repository is designed to be:
- ✅ Completely open-source (GPL-3.0)
- ✅ Fully functional (CPU-based)
- ✅ Secure against tier bypassing
- ✅ Clear in its limitations
- ✅ Effective marketing funnel to higher tiers

The protection comes from ARCHITECTURE, not obscurity.
Even if someone understands all mechanisms, they can't bypass them
because the GPU code literally doesn't exist in this repository.
