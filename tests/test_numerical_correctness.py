"""Independent numerical checks for the Tier 1 CPU backend.

These tests compare public computations with established NumPy/SciPy
reference implementations rather than comparing the implementation to itself.
"""

import numpy as np
from scipy import signal

from crystalline.backend import CPUBackend


backend = CPUBackend()


def _scipy_periodogram(data, fs, window):
    return signal.periodogram(
        np.asarray(data, dtype=np.float64),
        fs=fs,
        window=window,
        detrend=False,
        scaling="density",
        return_onesided=True,
    )


def test_spectral_analysis_matches_scipy_even_length():
    rng = np.random.default_rng(12345)
    data = rng.normal(size=128)
    fs = 200.0

    freqs, psd = backend.spectral_analysis(data, fs=fs, window="hann")
    ref_freqs, ref_psd = _scipy_periodogram(data, fs, "hann")

    np.testing.assert_allclose(freqs, ref_freqs, rtol=0.0, atol=1e-14)
    np.testing.assert_allclose(psd, ref_psd, rtol=1e-12, atol=1e-14)


def test_spectral_analysis_matches_scipy_odd_length():
    rng = np.random.default_rng(54321)
    data = rng.normal(size=127)
    fs = 100.0

    freqs, psd = backend.spectral_analysis(data, fs=fs, window="hamming")
    ref_freqs, ref_psd = _scipy_periodogram(data, fs, "hamming")

    np.testing.assert_allclose(freqs, ref_freqs, rtol=0.0, atol=1e-14)
    np.testing.assert_allclose(psd, ref_psd, rtol=1e-12, atol=1e-14)


def test_spectral_analysis_rejects_invalid_sampling_rate():
    data = np.ones(16)

    for fs in (0.0, -1.0):
        try:
            backend.spectral_analysis(data, fs=fs)
        except ValueError:
            pass
        else:
            raise AssertionError("non-positive sampling rates must be rejected")


def test_convolution_stride_is_applied():
    data = np.arange(8, dtype=float)
    kernel = np.array([1.0, 2.0, 1.0])

    expected = signal.convolve(data, kernel, mode="same")[::2]
    actual = backend.convolution(data, kernel, stride=2)

    np.testing.assert_allclose(actual, expected)


def test_convolution_rejects_nonpositive_stride():
    data = np.arange(8, dtype=float)
    kernel = np.array([1.0, 2.0, 1.0])

    for stride in (0, -1):
        try:
            backend.convolution(data, kernel, stride=stride)
        except ValueError:
            pass
        else:
            raise AssertionError("stride must be a positive integer")
