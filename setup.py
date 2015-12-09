# Time-stamp: <Thu 2015-12-10 00:00 svarrette>

"""Resif -- Revolutionary EasyBuild-based Software Installation Framework (RESIF).

Setuptools configuration file.

Resources:
- https://packaging.python.org/en/latest/distributing/
- https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
"""

from __future__ import print_function

# Preliminary checks that cannot be done by setuptools
# like... the setuptools dependency itself!
# Thanks [Serge and Pythran](https://github.com/serge-sans-paille/pythran) for suggesting that ;)
try:
    import setuptools
except ImportError:
    print()
    print("*****************************************************")
    print("* Setuptools must be installed before running setup *")
    print("*****************************************************")
    print()
    raise

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import codecs
import os
import sys
import re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

LONG_DESCRIPTION = None
README_MARKDOWN  = None

with open('README.md') as markdown_source:
    README_MARKDOWN = markdown_source.read()

if 'upload' in sys.argv:
    # Converts the README.md file to ReST, since PyPI uses ReST for formatting,
    # This allows to have one canonical README file, being the README.md
    # The conversion only needs to be done on upload.
    # Otherwise, the pandoc import and errors that are thrown when
    # pandoc are both overhead and a source of confusion for general
    # usage/installation.
    import pandoc
    pandoc.core.PANDOC_PATH = 'pandoc'
    doc = pandoc.Document()
    doc.markdown = README_MARKDOWN
    LONG_DESCRIPTION = doc.rst
else:
    # If pandoc isn't installed, e.g. when downloading from pip,
    # just use the regular README.
    LONG_DESCRIPTION = README_MARKDOWN


setup(
    name='resif',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=find_version('resif', '__init__.py'),

    # The project's main homepage.
    url='http://github.com/ULHPC/resif',

    description='Command line interface to deploy an EasyBuild-based software infrastructure and manage it.',
    long_description=LONG_DESCRIPTION,
    keywords='software build easybuild environment modules development',

    # Author details
    author='ULHPC Sysadmins Team',
    author_email='hpc-sysadmins@uni.lu',

    license='GPLv2',

    packages=['resif'],

    # Run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'click >= 3.3',
        'GitPython >= 0.3',
        'PyYaml >= 3.10',
    ],


    # List of classifiers the categorize your project.
    # For a full listing, see https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        # How mature is the project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Environment :: Console',
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points='''
        [console_scripts]
        resif=resif.resif:resif
    ''',
)
