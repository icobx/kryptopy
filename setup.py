from setuptools import setup

setup(
    name='kryptopy',
    version='0.1.0',
    description='Simple tool for file encryption/decryption.',
    url='https://github.com/icobx/kryptopy',
    author='icobx',
    author_email='jakub.fedorko@icloud.com',
    license='MIT',
    packages=['krypto'],
    install_requires=['pycryptodome'],
    entry_points={
        'console_scripts': [
            'kryptopy = main:main'
        ]},

)