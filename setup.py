#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
from distutils.core import setup

setup(
      name='lesscpy',
      version='0.9h',
      description='Lesscss compiler.',
      author='Jóhann T Maríusson',
      author_email='jtm@robot.is',
      keywords = ["lesscss"],
      url='https://github.com/robotis/lesscpy',
      packages=['lesscpy', 
                'lesscpy/lessc',
                'lesscpy/lib',
                'lesscpy/plib',
                'lesscpy/scripts',
                'lesscpy/test'],
      scripts = ['bin/lesscpy'],
      install_requires=["ply"],
      package_data={'lesscpy': ['lesscpy/test/css/*.css', 
                                'lesscpy/test/css/issues/*.css',
                                'lesscpy/test/less/*.less',
                                'lesscpy/test/less/issues/*.less',]},
      license=open('LICENSE').read(),
      long_description=open('README').read(),
)