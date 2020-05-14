#!/usr/bin/python3

from setuptools import find_packages, setup

setup(
    name='quasicode',
    version='0.4.0',
    author='witling',
    description='the best programming language around.',
    url='https://github.com/witling/quasicode',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'dill',
        'lark-parser',
    ],
    python_requires='>=3.5',
    entry_points={'console_scripts': ['qc=qc.__main__:main']}
)
