import setuptools

setuptools.setup(
    name='kryptopy-pkg-icobx',
    version='0.1.0',
    description='Simple tool for file encryption/decryption.',
    url='https://github.com/icobx/kryptopy',
    author='icobx',
    author_email='jakub.fedorko@icloud.com',
    license='MIT',
    packages=['krypto'],
    install_requires=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'kryptopy = main:main'
        ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)