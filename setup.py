#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
import pkg_resources

import codecs

import lesscpy

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = [
        str(req) for req in pkg_resources.parse_requirements(f)
    ]
with open("test-requirements.txt", "r") as f:
    test_requires = []
    for line in f.readlines():
        # Skip '-r ...' includes which pkg_resources doesn't understand:
        if not line.startswith('-r '):
            test_requires.append(str(pkg_resources.Requirement.parse(line)))

setup(
    name='lesscpy',
    version=lesscpy.__version__,
    license="MIT",
    description='Python LESS compiler',
    long_description=long_description,
    author='Jóhann T Maríusson',
    author_email='jtm@robot.is',
    url='https://github.com/lesscpy/lesscpy',
    packages=find_packages(exclude=['*test*']),
    package_data={'': ['LICENSE']},
    entry_points={
        'console_scripts': ['lesscpy = lesscpy.scripts.compiler:run']
    },
    install_requires=install_requires,
    tests_require=test_requires,
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Pre-processors',
    ],
)
