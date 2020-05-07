#!/usr/bin/python3

from setuptools import find_package, setup

setup(
    name='quasicode',
    version='0.0.1',
    description='the best programming language around.',
    packages=find_packages(),
    install_requires=[
        'dill'
    ],
    entry_points={'console_scripts': ['qc=qc.__main__:main']}
)
