"""
Example 1: Basic Spectral Analysis

This example demonstrates how to perform spectral analysis on a signal
using the Tier 1 CPU backend.
"""

import numpy as np
from crystalline import spectral_analysis
import matplotlib.pyplot as plt

# Create a composite signal with multiple frequencies
fs = 1000  # Sample rate: 1000 Hz
duration = 2  # seconds
t = np.arange(0, duration, 1/fs)

# Component signals
signal_50hz = np.sin(2 * np.pi * 50 * t)      # 50 Hz component
signal_120hz = 0.5 * np.sin(2 * np.pi * 120 * t)  # 120 Hz component
signal_250hz = 0.25 * np.sin(2 * np.pi * 250 * t) # 250 Hz component

# Combined signal
signal = signal_50hz + signal_120hz + signal_250hz

# Add some noise
noise = 0.1 * np.random.randn(len(t))
signal = signal + noise

print("📊 Spectral Analysis Example")
print(f"Sample rate: {fs} Hz")
print(f"Signal duration: {duration} seconds")
print(f"Signal components: 50 Hz, 120 Hz, 250 Hz")

# Perform spectral analysis
frequencies, power_spectra = spectral_analysis(signal, fs=fs, window='hann')

# Find peaks (dominant frequencies)
peak_indices = np.argsort(power_spectra)[-3:]
peak_freqs = frequencies[peak_indices]
peak_powers = power_spectra[peak_indices]

print("\nDominant frequencies detected:")
for i, (freq, power) in enumerate(zip(peak_freqs[::-1], peak_powers[::-1]), 1):
    print(f"  {i}. {freq:.1f} Hz (power: {power:.2e})")

# Optionally plot (requires matplotlib)
try:
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(t[:500], signal[:500])  # Show first 0.5 seconds
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Input Signal')
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.semilogy(frequencies[:len(frequencies)//2], power_spectra[:len(power_spectra)//2])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    plt.title('Power Spectral Density')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
except ImportError:
    print("\n(Install matplotlib to see plots: pip install matplotlib)")
