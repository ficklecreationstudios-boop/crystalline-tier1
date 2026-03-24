"""
Example 2: Signal Filtering

This example demonstrates how to filter signals using digital filters
in the frequency domain.
"""

import numpy as np
from crystalline import spectral_filtering, spectral_analysis

fs = 100  # Sample rate: 100 Hz
t = np.arange(0, 10, 1/fs)

# Create a noisy signal with low-frequency trend and high-frequency noise
# Low frequency component (interesting signal)
signal_low = 2 * np.sin(2 * np.pi * 2 * t)  # 2 Hz sine

# High frequency component (noise)
noise_high = 0.5 * np.sin(2 * np.pi * 30 * t)  # 30 Hz noise

# Combined noisy signal
noisy_signal = signal_low + noise_high + 0.1 * np.random.randn(len(t))

print("🔊 Signal Filtering Example")
print(f"Sample rate: {fs} Hz")
print(f"Original signal: 2 Hz sine wave")
print(f"Noise: 30 Hz sine wave + Gaussian")

# Analyze original signal
freqs_orig, psd_orig = spectral_analysis(noisy_signal, fs=fs)

# Apply low-pass filter to remove high-frequency noise
# Cutoff at 10 Hz - should preserve 2 Hz, remove 30 Hz
filtered_signal = spectral_filtering(
    noisy_signal,
    cutoff=10,
    order=4,
    btype='low'
)

# Analyze filtered signal
freqs_filt, psd_filt = spectral_analysis(filtered_signal, fs=fs)

print("\n✅ Low-pass filter applied (cutoff = 10 Hz, order = 4)")

# Calculate signal quality improvement
snr_original = 10 * np.log10(np.sum(signal_low**2) / np.sum(noise_high**2))
snr_filtered = 10 * np.log10(np.sum(signal_low**2) / np.sum(filtered_signal - signal_low)**2)

print(f"SNR improved: {snr_original:.2f} dB → {snr_filtered:.2f} dB")

# Other filter examples
print("\n📋 Other filter types:")

# Band-pass filter (between 1-5 Hz)
bandpass_signal = spectral_filtering(
    noisy_signal,
    cutoff=[1, 5],
    order=4,
    btype='band'
)
print("  ✓ Band-pass (1-5 Hz)")

# High-pass filter (above 5 Hz)
highpass_signal = spectral_filtering(
    noisy_signal,
    cutoff=5,
    order=4,
    btype='high'
)
print("  ✓ High-pass (5 Hz)")

# Band-stop filter (reject 28-32 Hz)
bandstop_signal = spectral_filtering(
    noisy_signal,
    cutoff=[28, 32],
    order=4,
    btype='bandstop'
)
print("  ✓ Band-stop (28-32 Hz)")

print("\n💡 Tip: Different filter orders affect transition steepness")
print("   Higher order = steeper transition, but might introduce artifacts")
print("   Typical range: order 2-8")

print("\nDone! ✨")
