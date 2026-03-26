#!/usr/bin/env python

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
    url="https://github.com/nohikomiso/saxo-openapi",
    packages=find_packages(include=["saxo_openapi", "saxo_openapi.*"]),
    include_package_data=True,
    install_requires=["requests"],
    python_requires=">=3.13",
    zip_safe=False,
    keywords="saxo_openapi",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
    ],
)
