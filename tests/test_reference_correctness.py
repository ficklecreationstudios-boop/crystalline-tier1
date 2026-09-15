"""Reference checks for the remaining Tier 1 numerical wrappers."""

import numpy as np
from scipy import linalg, signal

from crystalline.backend import CPUBackend


backend = CPUBackend()


def test_filtering_matches_scipy_reference():
    x = np.sin(np.linspace(0.0, 40.0, 500)) + 0.25 * np.sin(np.linspace(0.0, 400.0, 500))

    expected_b, expected_a = signal.butter(4, 0.2, btype="low")
    expected = signal.filtfilt(expected_b, expected_a, x)
    actual = backend.spectral_filtering(x, cutoff=0.2, order=4, btype="low")

    np.testing.assert_allclose(actual, expected, rtol=1e-12, atol=1e-12)


def test_linear_solve_matches_scipy_reference():
    A = np.array([[4.0, 1.0, 2.0], [1.0, 5.0, 0.5], [2.0, 0.5, 6.0]])
    b = np.array([7.0, 4.0, 9.0])

    expected = linalg.solve(A, b)
    actual = backend.linear_algebra_solve(A, b)

    np.testing.assert_allclose(actual, expected, rtol=1e-13, atol=1e-13)


def test_matrix_multiply_matches_numpy_reference():
    A = np.arange(12, dtype=float).reshape(3, 4)
    B = np.arange(20, dtype=float).reshape(4, 5)

    np.testing.assert_allclose(backend.matrix_multiply(A, B), np.matmul(A, B))
