#!/usr/bin/env python3
"""Compatibility setup script for the CPU-only Crystalline Tier 1 package."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="crystalline-tier1",
    version="5.0.1",
    author="Crystalline Project Contributors",
    description="CPU numerical and signal-processing utilities for the Crystalline Tier 1 edition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ficklecreationstudios-boop/crystalline-tier1",
    project_urls={
        "Bug Tracker": "https://github.com/ficklecreationstudios-boop/crystalline-tier1/issues",
        "Documentation": "https://github.com/ficklecreationstudios-boop/crystalline-tier1/tree/main/docs",
        "Source Code": "https://github.com/ficklecreationstudios-boop/crystalline-tier1",
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
        "Development Status :: 4 - Beta",
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
    keywords="spectral analysis signal processing linear algebra cpu scientific computing",
    include_package_data=True,
    zip_safe=False,
)
