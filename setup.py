#!/usr/bin/env python

from setuptools import setup

setup(
        name='VCSUtils',
        version='0.0.1',
        description='Work with major VCS tools in the abstract.',
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
                'vcs=vcsutils.cli:main',
                ]
            },
        packages=[
            'vcsutils',
            ],
        )
