#! /usr/bin/env python3
""" Setuptools-based setup script. To install, type:

    python setup.py install

"""

from setuptools import setup, find_packages
import versioneer

try:
    with open("README.md", "r") as handle:
        long_description = handle.read()
except:
    long_description = None


setup(
    name='flamel',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='CLI tool for analyzing alchemical free energy calculcations',
    maintainer='Oliver Beckstein',
    maintainer_email='orbeckst@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows ',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
    ],
    packages=find_packages(),
    license='BSD',
    long_description = long_description,
    long_description_content_type='text/markdown',
    roject_urls={'Source': 'https://github.com/alchemistry/flamel'},
    install_requires=['numpy', 'alchemlyb', 'pandas>=1.2,!=1.3.0'],
    entry_points={
        'console_scripts': [
            'flamel=flamel.flamel:main'
        ]
    }
)
