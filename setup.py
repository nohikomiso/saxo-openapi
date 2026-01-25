#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup  # type: ignore

setup_requirements: list[str] = []

setup(
    name="saxo_openapi",
    version="0.1.0",
    description="SAXO Bank OpenAPI REST-API access",
    long_description="",
    author="SAXO Bank",
    author_email="",
    url="",
    packages=find_packages(include=["saxo_openapi", "saxo_openapi.*"]),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.6",
    zip_safe=False,
    keywords="saxo_openapi",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
