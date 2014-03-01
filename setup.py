#!/usr/bin/env python
from distutils.core import setup

setup(
    name='stocker',
    version='0.2.0',
    author='donpiekarz, lisu',
    author_email='mateusz.lis@gmail.com', #TODO: create group for stocker
    packages=['stocker', 'stocker.common', 'stocker.SEP', \
            'stocker.SRV', 'stocker.SSP', 'stocker.test'],

    scripts=['bin/SEP.py', 'bin/SRV.py', 'bin/SSP.py'],

    url='http://pypi.python.org/pypi/stocker/',
    license='LICENSE.txt',
    description='''
    Allows to easily create stock exchange investment strategy and benchmark it on
    real stock exchange data (some data sets are included in release).
    Strategies can be implemented using Python programming language''',

    long_description=open('README.txt').read(),
    install_requires=["matplotlib >= 1.2.0"],
)
