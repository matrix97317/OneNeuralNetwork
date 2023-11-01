# -*- coding: utf-8 -*-
"""The setup.py for One Neural Network."""
from pkg_resources import parse_requirements
from setuptools import find_packages
from setuptools import setup


# Parse content from `README.md` as long description.
with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

# Parse content from `requirements.txt` as install requires.
with open("requirements.txt", encoding="utf-8") as fh:
    install_requires = [str(requirement) for requirement in parse_requirements(fh)]

setup(
    author="matrix97317",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
    ],
    description="This is a cross-chip platform collection of \
        operators and a unified neural network library.",
    entry_points={},
    install_requires=install_requires,
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="onn",
    packages=find_packages(exclude=["dist.*", "dist", "tests.*", "tests"]),
    python_requires=">=3.8",
    url="https://github.com/matrix97317/OneNerualNetwork",
)
