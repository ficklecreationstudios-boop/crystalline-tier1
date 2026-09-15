"""Smoke tests for the repository's executable examples."""

from pathlib import Path
import subprocess
import sys


EXAMPLES = [
    "1_spectral_analysis.py",
    "2_filtering.py",
    "3_linear_algebra.py",
    "4_tier_access.py",
]


def test_examples_execute_successfully():
    root = Path(__file__).resolve().parents[1]
    for name in EXAMPLES:
        result = subprocess.run(
            [sys.executable, str(root / "examples" / name)],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        assert result.returncode == 0, f"{name} failed:\n{result.stdout}\n{result.stderr}"
