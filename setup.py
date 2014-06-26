
from distutils.core import setup
setup(name='spdx',
    version='0.1',
    description='SPDX tag/value and RDF tools',
    packages=['spdx', 'spdx.parsers', 'spdx.writers', 'spdx.parsers.lexers'],
    author='Ahmed H. Ismail',
    author_email='ahm3d.hisham@gmail.com',
    url='http://git.spdx.org/?p=spdx-tools-python.git',
    package_data={'spdx' : ['spdx_licenselist.csv']},
    license='Apache-2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7'
        ]
    )