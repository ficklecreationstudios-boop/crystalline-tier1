"""Legacy setuptools entry point; project metadata lives in pyproject.toml."""

from setuptools import setup

# Keep a single source of truth for package metadata.  Modern builds consume
# pyproject.toml; this compatibility shim intentionally contains no duplicate
# version, dependency, URL, or classifier declarations that could drift.
setup()
