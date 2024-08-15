#!/usr/bin/env python3
"""
Setup script for the Quadratic Equation Solver and Visualizer.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="quadratic-equation-solver",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive Python tool for solving quadratic equations and visualizing their graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quadratic-equations",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "quadratic-solver=main:main",
            "quadratic-demo=demo:main",
        ],
    },
    keywords="quadratic equation solver mathematics visualization education",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/quadratic-equations/issues",
        "Source": "https://github.com/yourusername/quadratic-equations",
        "Documentation": "https://github.com/yourusername/quadratic-equations#readme",
    },
)
