# -*- coding: utf-8 -*-
"""
"""
from distutils.core import setup

setup(
      name='lesscpy',
      version='0.6',
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
      package_data={'lesscpy': ['lesscpy/less.ast', 
                                'lesscpy/test/css/*.css', 
                                'lesscpy/test/css/issues/*.css',
                                'lesscpy/test/less/*.less',
                                'lesscpy/test/less/issues/*.less',]},
      license='LICENSE',
      long_description=open('README').read(),
)