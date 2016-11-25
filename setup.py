#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from setuptools import setup


setup(
    name='spdx-tools',
    version='0.2',
    description='SPDX parser and tools.',
    packages=['spdx', 'spdx.parsers', 'spdx.writers', 'spdx.parsers.lexers'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ply',
        'rdflib'
    ],
    test_requires=[
        'nose',
    ],

    author='Ahmed H. Ismail',
    author_email='ahm3d.hisham@gmail.com',
    maintainer='Philippe Ombredanne and SPDX group at the Linux Foundation and others',
    maintainer_email='pombredanne@gmail.com',
    url='https://github.com/spdx/tools-python',
    package_data={'spdx': ['spdx_licenselist.csv']},
    license='Apache-2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7'
    ]
)
