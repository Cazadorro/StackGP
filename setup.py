#!/usr/bin/env python

from distutils.core import setup

setup(name='StackGeneticProgramming',
      version='1.0',
      description='Stack Based Genetic Programming utilities',
      author='Cazadorro',
      author_email='...',
      url='https://github.com/Cazadorro/StackGP',
      packages=["stackgp"],
      include_package_data=True,
      install_requires=[
          "numpy",
      ],
      )
