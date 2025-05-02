#!/usr/bin/env python3

from setuptools import setup

setup(name= 'Forrest',
      version= '1.0',
      packages= ['Forrest'],
      entry_points= {
          'console_scripts' : [
              'Forrest = Forrest.cli:main'
          ]
      })