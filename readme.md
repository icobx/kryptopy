# kryptopy

## Contents

**Simple tool for file encryption / decryption.**

Done as an assignment #2 for [I-UPB](https://is.stuba.sk/katalog/syllabus.pl?predmet=282080;lang=en) course (FEI STU).


* **Usage**: 
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

* **Getting Started**
  - installation & prerequisites
  - how to run examples and tests
    - include a `Procfile` to start any necessary servers or daemon processes
  - location of:
    - code
    - issue tracker
    - wiki
    - blog posts, screencasts, etc
    - compiled documentation (add the project to [rdoc.info](http://rdoc.info))
    - travis-ci results
    - mailing list

* **Design Goals**
  - lightweight or full-featured?
  - performance, flexibility, expressiveness?

* **Detailed Usage**
  - models and interface
  - examples
  - configuration
  - middleware or plugins
  - how it works

* **Comparable Tools**

* **Developer info**
  - Important Components
  - layout of internal code tree
  - Limitations and known issues
  - performance and benchmarking

* **Colophon**
  - Credits -- everyone who has contributed code, libraries from which we've borrowed code.
  - Copyright and License -- state the license type (typically "Apache 2.0" or "All Rights Reserved and Confidential") and refer to the `LICENSE.md` file. Don't paste the license contents in here.
  - How to contribute
  - References

## Formatting

* Call the file `README.md`.
* Write in markdown format.
  - You should use triple backtick blocks for code, and supply a language prefix:

        ```ruby
        def hello(str)
          puts "hello #{str}!"
        end
        ```

* Do not wrap lines. In emacs, enable the `longlines-mode` to make your document word wrap intelligently.




## Supporting Documentation

Besides a `README.md`, your repo should contain a `CHANGELOG.md` summarizing major code changes, a `LICENSE.md` describing the code's license (typically Apache 2.0 for our open-source projects, All Rights Reserved for internal projects), and a `notes/` directory that is a git submodule of the project's wiki. See the [style guide for repo organization](https://github.com/infochimps-labs/style_guide/blob/master/style-guide-for-repo-organization.md) for more details.
