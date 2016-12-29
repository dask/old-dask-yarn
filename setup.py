#!/usr/bin/env python

from os.path import exists
from setuptools import setup

setup(name='dask_yarn',
      version='0.1.0',
      description='Dask on Yarn',
      url='http://github.com/dask/dask-yarn/',
      maintainer='Matthew Rocklin',
      maintainer_email='mrocklin@gmail.com',
      license='BSD',
      keywords='',
      packages=['dask_yarn'],
      install_requires=['knit', 'distributed', 'dask'],
      long_description=(open('README.md').read() if exists('README.md')
                        else ''),
      zip_safe=False)
