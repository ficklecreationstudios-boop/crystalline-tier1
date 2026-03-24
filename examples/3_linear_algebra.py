"""
Example 3: Linear Algebra

This example demonstrates CPU-based linear algebra operations
available in Tier 1.
"""

import numpy as np
from crystalline import get_backend

print("📐 Linear Algebra Example")
print("=" * 50)

# Get the Tier 1 CPU backend
backend = get_backend()
print(f"Backend: {backend.device}")
print(f"GPU Available: {backend.gpu_available}")
print(f"Tier: {backend.tier}")

print("\n1️⃣  Matrix Multiplication")
print("-" * 50)

# Create sample matrices
A = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
], dtype=np.float64)

B = np.array([
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
], dtype=np.float64)

print("Matrix A:")
print(A)
print("\nMatrix B:")
print(B)

# Multiply matrices
C = backend.matrix_multiply(A, B)
print("\nResult (A @ B):")
print(C)

print("\n2️⃣  Solving Linear Systems")
print("-" * 50)

# Create a system: Ax = b
A_system = np.array([
    [3, 2, 1],
    [1, 4, 2],
    [2, 1, 3]
], dtype=np.float64)

b = np.array([14, 17, 10], dtype=np.float64)

print("Solving: A @ x = b")
print("A =")
print(A_system)
print("\nb =", b)

# Solve
x = backend.linear_algebra_solve(A_system, b)
print("\nSolution x =", x)

# Verify
residual = np.linalg.norm(A_system @ x - b)
print(f"Residual (verification): {residual:.2e}")

print("\n3️⃣  Convolution")
print("-" * 50)

# Example: smooth a signal with a kernel
signal = np.array([1, 0, 2, 0, 3, 0, 4, 0, 5], dtype=np.float64)
kernel = np.array([0.25, 0.5, 0.25], dtype=np.float64)  # Smoothing kernel

print("Signal:", signal)
print("Kernel:", kernel)

# Convolve
smoothed = backend.convolution(signal, kernel, padding=1)
print("Smoothed:", smoothed)

print("\n✅ All operations completed!")
print("💡 Tier 1 uses NumPy/SciPy for efficient CPU computation")
print("   For GPU acceleration, upgrade to Tier 2+")
