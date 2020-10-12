# kryptopy

**Simple tool for file encryption / decryption.**

Done as an assignment #2 for [I-UPB](https://is.stuba.sk/katalog/syllabus.pl?predmet=282080;lang=en) course (FEI STU).


## Usage: 
  - `kryptopy [-h] [-d] infile keyfile outfile`

## Getting Started:

- **Prerequisites**
    - python _>= 3.8_
    - pip
    
- **Installation**
    - `pip install kryptopy-x-py3-none-any.whl` or `kryptopy-x.tar.gz`
    - current version: `x = 0.0.6`
    
    
## Detailed Usage:

  - To **encrypt** a file, simply type `kryptopy` to command line followed by: 
    - a file to be encrypted, 
    - a file where encryption key will be stored,
    - and finally a file where encrypted data will be stored  
    
  - **Decryption** works the same way but option `-d, --decrypt` need to be used. Positional arguments in this mode mean:
    - a file to be decrypted,
    - a file with valid encryption key (key you received after encrypting)
    - and also a file where decrypted data will be stored
  
  - Help `-h, --help`:
      ```bash
        kryptopy [-h] [-d] infile keyfile outfile
        
        positional arguments:
          infile         file to be encrypted ( -d: decrypted )
          keyfile        encryption key will be stored here ( if non-existing is provided, new file will be created | -d:
                         existing must be provided )
          outfile        encrypted file will be stored here ( if non-existing is provided, new file will be created | -d:
                         decrypted )
        
        optional arguments:
          -h, --help     show this help message and exit
          -d, --decrypt  decryption mode ( valid 128 bit key must be provided )
       ```

## License

MIT © [icobx](https://github.com/icobx)
