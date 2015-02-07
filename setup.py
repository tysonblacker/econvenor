#!/usr/bin/env python
"""A virtual convenor https://www.econvenor.org."""
from setuptools import setup, find_packages

setup(
    name='econvenor',
    version='0.1a1',
    description=__doc__,
    long_description=open('README.rst').read(),
    author='eConvenor',
    author_email='mail@econvenor.org',
    url='https://www.econvenor.org/',
    packages=find_packages(),
    install_requires=[
        'Django',
        'South',
        'reportlab',
        'psycopg2',
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP",
    ],
    scripts=[
        'manage.py',
    ],
)
