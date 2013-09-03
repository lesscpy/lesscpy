#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
from distutils.core import setup
import codecs

with codecs.open('LICENSE', encoding="utf-8") as f:
    license = f.read()
with codecs.open('README.rst', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='lesscpy',
    version='0.9j',
    description='Lesscss compiler.',
    author='Jóhann T Maríusson',
    author_email='jtm@robot.is',
    keywords=["lesscss"],
    url='https://github.com/robotis/lesscpy',
    packages=['lesscpy',
              'lesscpy/lessc',
              'lesscpy/lib',
              'lesscpy/plib',
              'lesscpy/scripts',
              'lesscpy/test'],
    scripts=['bin/lesscpy'],
    install_requires=["ply"],
    package_data={'lesscpy': ['lesscpy/test/css/*.css',
                              'lesscpy/test/css/issues/*.css',
                              'lesscpy/test/less/*.less',
                              'lesscpy/test/less/issues/*.less']},
    license=license,
    long_description=long_description,
)
