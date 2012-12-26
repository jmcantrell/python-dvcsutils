#!/usr/bin/env python

from setuptools import setup

setup(
        name='DVCSUtils',
        version='0.0.5',
        description='Work with major DVCS tools in the abstract.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            ],
        install_requires=[
            ],
        entry_points={
            'console_scripts': [
                'dvcs=dvcsutils.cli:main',
                ]
            },
        packages=[
            'dvcsutils',
            ],
        )
