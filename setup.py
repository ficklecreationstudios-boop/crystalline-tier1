#!/usr/bin/env python3
"""
Setup script for Crystalline GPU - Tier 1 (Free Edition)

This package contains CPU-only implementations suitable for learning
and research. GPU acceleration and advanced features require paid tiers.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="crystalline-tier1",
    version="5.0.0",
    author="Crystalline Project",
    author_email="[CONTACT_EMAIL]",
    description="Crystalline GPU - Tier 1 (Free, CPU-only edition)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/crystalline-tier1",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/crystalline-tier1/issues",
        "Documentation": "https://github.com/yourusername/crystalline-tier1/docs",
        "Source Code": "https://github.com/yourusername/crystalline-tier1",
    },
    packages=find_packages(exclude=["tests", "docs", "benchmarks"]),
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "viz": [
            "matplotlib>=3.3.0",
            "TensorBoard>=2.4.0",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="gpu acceleration cpu computing spectral analysis linear algebra",
    include_package_data=True,
    zip_safe=False,
)
