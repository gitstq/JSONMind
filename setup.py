#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONMind Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

setup(
    name="jsonmind",
    version="1.0.0",
    author="JSONMind Team",
    author_email="contact@jsonmind.dev",
    description="🧠 Lightweight JSON Data Intelligence Processing & Visualization Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/JSONMind",
    py_modules=["jsonmind"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "jsonmind=jsonmind:main",
        ],
    },
    keywords="json, validation, transformation, query, visualization, cli, developer-tools",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/JSONMind/issues",
        "Source": "https://github.com/gitstq/JSONMind",
        "Documentation": "https://github.com/gitstq/JSONMind#readme",
    },
)
