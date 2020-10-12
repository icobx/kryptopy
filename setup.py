import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='kryptopy',
    version='0.0.6',
    description='Simple tool for file encryption/decryption.',
    long_description=long_description,
    url='https://github.com/icobx/kryptopy',
    author='icobx',
    author_email='jakub.fedorko@icloud.com',
    license='MIT',
    packages=['krypto', 'utility'],
    install_requires='pycryptodome >= 3.9.8',
    entry_points={
        'console_scripts': [
            'kryptopy = krypto.__main__:main'
        ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)