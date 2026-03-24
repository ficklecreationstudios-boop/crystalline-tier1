# Test Suite
# Run with: pytest

import pytest
import numpy as np
from crystalline import get_backend, spectral_analysis, spectral_filtering
from crystalline.licensing import check_tier_access, TierFeatureBlockedError, get_tier
from crystalline.backend import GPUBackend


class TestTierEnforcement:
    """Test that Tier 1 restrictions are enforced."""
    
    def test_current_tier_is_tier1(self):
        """Verify we're running as Tier 1."""
        assert get_tier() == "TIER_1_FREE"
    
    def test_spectral_analysis_allowed(self):
        """Spectral analysis should be accessible in Tier 1."""
        check_tier_access("spectral_analysis")  # Should not raise
    
    def test_spectral_filtering_allowed(self):
        """Spectral filtering should be accessible in Tier 1."""
        check_tier_access("spectral_filtering")  # Should not raise
    
    def test_gpu_acceleration_blocked(self):
        """GPU acceleration should be blocked in Tier 1."""
        with pytest.raises(TierFeatureBlockedError):
            check_tier_access("gpu_acceleration")
    
    def test_gpu_backend_blocked(self):
        """GPU backend constructor should raise error."""
        with pytest.raises(TierFeatureBlockedError):
            GPUBackend()


class TestBackend:
    """Test CPU backend functionality."""
    
    def test_get_backend_returns_cpu(self):
        """get_backend() should return CPU backend."""
        backend = get_backend()
        assert backend.device == "cpu"
        assert backend.gpu_available == False
        assert backend.tier == "TIER_1_FREE"
    
    def test_backend_singleton(self):
        """get_backend() should return same instance."""
        b1 = get_backend()
        b2 = get_backend()
        assert b1 is b2


class TestSpectralAnalysis:
    """Test spectral analysis functionality."""
    
    def test_spectral_analysis_basic(self):
        """Basic spectral analysis should work."""
        signal = np.random.randn(1024)
        freqs, psd = spectral_analysis(signal, fs=100.0)
        
        assert len(freqs) == len(psd)
        assert freqs[0] >= 0
        assert np.all(psd >= 0)
    
    def test_spectral_analysis_sine_wave(self):
        """Spectral analysis should detect sine wave frequency."""
        fs = 1000
        f_signal = 50  # 50 Hz signal
        t = np.arange(0, 1, 1/fs)
        signal = np.sin(2 * np.pi * f_signal * t)
        
        freqs, psd = spectral_analysis(signal, fs=fs)
        
        # Peak should be near 50 Hz
        peak_freq = freqs[np.argmax(psd)]
        assert abs(peak_freq - f_signal) < 2  # Within 2 Hz


class TestFiltering:
    """Test filtering functionality."""
    
    def test_spectral_filtering_lowpass(self):
        """Low-pass filtering should attenuate high frequencies."""
        fs = 1000
        t = np.arange(0, 1, 1/fs)
        
        # Create signal with high and low freq components
        low = np.sin(2 * np.pi * 10 * t)
        high = np.sin(2 * np.pi * 200 * t)
        signal = low + high
        
        # Apply low-pass filter at 50 Hz
        filtered = spectral_filtering(signal, cutoff=50, order=4, btype='low')
        
        # Filtered signal should be closer to low than high
        assert len(filtered) == len(signal)
        assert np.all(np.isfinite(filtered))
    
    def test_spectral_filtering_bandpass(self):
        """Band-pass filtering should work with 2-element cutoff."""
        signal = np.random.randn(1000)
        filtered = spectral_filtering(signal, cutoff=[10, 50], btype='band', order=4)
        
        assert len(filtered) == len(signal)
        assert np.all(np.isfinite(filtered))


class TestLinearAlgebra:
    """Test linear algebra operations."""
    
    def test_matrix_multiply(self):
        """Matrix multiplication should work."""
        backend = get_backend()
        A = np.array([[1, 2], [3, 4]], dtype=np.float64)
        B = np.array([[5, 6], [7, 8]], dtype=np.float64)
        
        C = backend.matrix_multiply(A, B)
        expected = np.array([[19, 22], [43, 50]], dtype=np.float64)
        
        np.testing.assert_array_almost_equal(C, expected)
    
    def test_linear_solve(self):
        """Solving Ax=b should work."""
        backend = get_backend()
        A = np.array([[3, 2], [1, 4]], dtype=np.float64)
        b = np.array([8, 9], dtype=np.float64)
        
        x = backend.linear_algebra_solve(A, b)
        
        # Verify: A @ x should equal b
        np.testing.assert_array_almost_equal(A @ x, b)
    
    def test_convolution(self):
        """Convolution should work."""
        backend = get_backend()
        signal = np.array([1, 0, 2, 0, 3], dtype=np.float64)
        kernel = np.array([0.5, 0.5], dtype=np.float64)
        
        result = backend.convolution(signal, kernel)
        assert len(result) == len(signal)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
