"""
Example 2: Signal Filtering

The public Tier 1 filtering API uses SciPy's normalized digital-filter
convention because it does not accept a sampling-frequency argument.
"""

import numpy as np
from crystalline import spectral_filtering, spectral_analysis

fs = 100  # Sample rate: 100 Hz
t = np.arange(0, 10, 1 / fs)

signal_low = 2 * np.sin(2 * np.pi * 2 * t)       # 2 Hz signal
noise_high = 0.5 * np.sin(2 * np.pi * 30 * t)    # 30 Hz component
noisy_signal = signal_low + noise_high + 0.1 * np.random.randn(len(t))

print("Signal Filtering Example")
print(f"Sample rate: {fs} Hz")
print("Signal: 2 Hz sine wave")
print("High-frequency component: 30 Hz sine wave + Gaussian noise")

spectral_analysis(noisy_signal, fs=fs)

# A normalized cutoff of 0.20 corresponds to 10 Hz because Nyquist is 50 Hz.
filtered_signal = spectral_filtering(
    noisy_signal,
    cutoff=0.20,
    order=4,
    btype="low",
)

spectral_analysis(filtered_signal, fs=fs)
print("\nLow-pass filter applied (cutoff = 10 Hz / normalized 0.20)")

# 1-5 Hz corresponds to normalized cutoffs [0.02, 0.10].
bandpass_signal = spectral_filtering(
    noisy_signal,
    cutoff=[0.02, 0.10],
    order=4,
    btype="band",
)
print("Band-pass: 1-5 Hz (normalized [0.02, 0.10])")

# Above 5 Hz corresponds to a normalized cutoff of 0.10.
highpass_signal = spectral_filtering(
    noisy_signal,
    cutoff=0.10,
    order=4,
    btype="high",
)
print("High-pass: above 5 Hz (normalized 0.10)")

# 28-32 Hz corresponds to normalized cutoffs [0.56, 0.64].
bandstop_signal = spectral_filtering(
    noisy_signal,
    cutoff=[0.56, 0.64],
    order=4,
    btype="bandstop",
)
print("Band-stop: 28-32 Hz (normalized [0.56, 0.64])")

print("\nDone.")
