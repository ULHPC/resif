from setuptools import setup

setup(
    name='resif',
    version='0.1',
    author='Maxime Schmitt',
    author_email='maxime.schmitt@ext.uni.lu',
    url='url/to/PyPi/page',
    description='Command line interface to deploy an EasyBuild infrastructure and manage it.',
    long_description='This module has been developped by the University of Luxembourg in order to improve the management of its clusters. This application will help you easily deploy an EasyBuild installation and deploy software on it, in a heavily automated way.',
    classifiers=[
    'Programming Language :: Python',
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
        'click',
        'GitPython',
        'PyYaml',
    ],
    entry_points='''
        [console_scripts]
        resif=resif:resif
    ''',
)
