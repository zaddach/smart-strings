#!/usr/bin/env python3
from distutils.core import setup

setup(
    name='smart-strings',
    version='0.0.1',
    author='Jonas Zaddach',
    author_email='zaddach@eurecom.fr',
    py_modules=['smart_strings'],
    url='https://github.com/zaddach/smart-strings',
    license='MIT',
    description='A smarter version of the unix strings utility',
    long_description=open('README.md').read()
)
