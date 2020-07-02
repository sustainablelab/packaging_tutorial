#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

# Show README.md as PyPI "Project description".
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# open with utf-8 encoding for tree symbols: └─, ├─, etc.

setuptools.setup(
    name="example_pkg_mostly_upright", # no dashes in name!
    version="0.0.4", # must increment this to re-upload
    author="Mike Gazes",
    author_email="sustainablelab@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sustainablelab/packaging_tutorial",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    install_requires=[
        # "pygame",
        ]
)
