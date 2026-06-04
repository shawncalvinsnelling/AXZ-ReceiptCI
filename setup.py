#!/usr/bin/env python3
"""Backward-compatible setuptools shim for AXZ ReceiptCI.

The canonical package metadata lives in pyproject.toml. This file exists only
for older tooling that still expects setup.py to be present.
"""

from setuptools import find_packages, setup


setup(
    name="axz-receiptci",
    version="1.2.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "axz-receiptci=axz_receiptci.cli:main",
        ],
    },
)
