from setuptools import setup, find_packages

setup(
    name='lagrange-cli',
    install_requires= [
        "requests>=2.28.0"
    ],
    version='1.0',
    description='A CLI tool that allows you to interact with datasets, models, and spaces all from the command line.',
    entry_points={
        'console_scripts': [
            'swan = swan.cli:main',
        ]
    },
    packages=find_packages(),
)
