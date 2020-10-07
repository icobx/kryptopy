from setuptools import setup

setup(
    name='kryptopy',
    version='0.1.0',
    packages=['krypto'],
    entry_points={
        'console_scripts': [
            'kryptopy = main:main'
        ]
    })