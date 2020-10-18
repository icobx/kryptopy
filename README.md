# kryptopy

**Simple tool for file encryption / decryption.**

Done as an assignment #2 for [I-UPB](https://is.stuba.sk/katalog/syllabus.pl?predmet=282080;lang=en) course (FEI STU).


## Usage: 
  - `kryptopy g [-h] [-d] infile keyfile outfile`
  - `g` stands for GCM mode, there 4 modes available

## Getting Started:

- **Prerequisites**
    - python _>= 3.8_
    - pip
    
- **Installation**
    - `pip install kryptopy-x-py3-none-any.whl` or `kryptopy-x.tar.gz`
    - current version: `x = 0.1.0`
    
    
## Detailed Usage:

  - There are 4 modes available  
  
  - Help `-h, --help`:
      ```bash
        usage: kryptopy [-h] {g,a,s,gen} ...

        optional arguments:
            -h, --help   show this help message and exit

        modes:
           {g,a,s,gen} followed by -h, --help to show help for given mode
            g          AES-GCM hybrid encryption / decryption mode
            a          asymmetric PKCS1_OAEP encryption / decryption mode
            s          AES-CTR symmetric encryption / decryption mode
            gen        mode for generating RSA key-pair
       ```
  - Single-letter modes are all encryption modes but all have `[-d, --decrypt]` switch for decryption too

  - To encrypt a file, type `kryptopy {g,a,s} infile keyfile [outfile]` to command line:
    - `infile` is file to be encrypted,
    - `keyfile` is file with public part of RSA key[^s],
    - `[outfile]` is file where encrypted data will be stored (optional: if omitted, will be replaced by arbitrary name)
    
    [^s]: `s` mode does not use RSA, you only need to provide file for randomly generated key
    
- To decrypt a file, type `kryptopy {g,a,s} [-d, --decrypt] infile keyfile [outfile]` to command line:
    - `infile` is file to be decrypted,
    - `keyfile` is file with private part of RSA key[^sd],
    - `[outfile]` is file where decrypted data will be stored (optional: if omitted, will be replaced by arbitrary name)

    [^sd]: `s` mode does not use RSA, you need to provide file with key you received when encrypting

 - Help `g -h, --help` of the AES-GCM hybrid mode:
    ```
    usage: kryptopy g [-h] [-d] infile keyfile [outfile]

    positional arguments:
      infile         file to be encrypted ( -d: decrypted )
      keyfile        public key for encryption of symmetric cipher key ( -d: private key for decryption )
      outfile        encrypted data will be stored here, if non-existing is provided, new file will be created ( default: hybrid_outfile, -d: decrypted )

    optional arguments:
      -h, --help     show this help message and exit
      -d, --decrypt  decryption mode
   ```

  - Mode for generating RSA key-pair only takes 2 arguments, `public_key` and `private_key`.
  - Help `gen -h, --help` for RSA key-pair generating mode:
      ```
    usage: kryptopy gen [-h] public_key private_key

    positional arguments:
        public_key   public key will be store here
        private_key  private key will be store here

    optional arguments:
        -h, --help   show this help message and exit
    ``` 
## License

MIT © [icobx](https://github.com/icobx)
