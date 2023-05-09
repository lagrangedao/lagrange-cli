from setuptools import setup, find_packages

setup(
    name='lagrange-cli',
    install_requires= [
        "requests>=2.28.0"
    ],
    version='1.1',
    description='A CLI tool that allows you to interact with lagrange datasets, models, and spaces all from the command line.',
    package_data={'': ['config.json', 'data.json']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'swan = swan.cli:main',
        ]
    },
    packages=find_packages(),
)
