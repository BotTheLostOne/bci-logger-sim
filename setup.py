"""Setup script for BCI Logger Simulator package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="bci-logger-sim",
    version="0.1.0",
    author="Bot The Lost One",
    description="BCI logger simulator: generates and logs synthetic neural signals for research and gaming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BotTheLostOne/bci-logger-sim",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Games/Entertainment :: Role-Playing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
        ],
    },
    keywords="bci neuroscience eeg spikes simulation gaming dnd brain",
    project_urls={
        "Bug Reports": "https://github.com/BotTheLostOne/bci-logger-sim/issues",
        "Source": "https://github.com/BotTheLostOne/bci-logger-sim",
    },
)
