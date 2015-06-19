from setuptools import setup

setup(
    name='resif',
    version='1.4.1',
    author='ULHPC',
    author_email='hpc-sysadmins@uni.lu',
    maintainer='ULHPC',
    maintainer_email='hpc-sysadmins@uni.lu',
    url='https://hpc.uni.lu/',
    license='GPLv2',
    description='Command line interface to deploy an EasyBuild infrastructure and manage it.',
    long_description='This module has been developped by the University of Luxembourg in order to improve the management of its clusters. This application will help you easily deploy an EasyBuild installation and deploy software on it, in a heavily automated way.',
    classifiers=[
    'License :: OSI Approved',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Operating System :: Unix',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Topic :: Scientific/Engineering',
    'Topic :: System :: Installation/Setup',
    'Topic :: System :: Systems Administration',
    'Topic :: Utilities',
    'Natural Language :: English',
    'Intended Audience :: Science/Research',
    'Intended Audience :: System Administrators',
    'Environment :: Console',
    ],
    packages=['resif'],
    install_requires=[
        'click >= 3.3',
        'GitPython >= 0.3',
        'PyYaml >= 3.10',
    ],
    entry_points='''
        [console_scripts]
        resif=resif.resif:resif
    ''',
)
