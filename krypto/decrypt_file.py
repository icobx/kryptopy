import os
import timeit

from Crypto.Cipher import AES
from Crypto.Util import Counter
from .utility.bcolors import bcolors


def decrypt_file(in_filename, key_filename, out_filename=None):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        # nonce was added unencrypted at the beginning, sizeof(8 bytes)
        nonce = infile.read(8)
        counter_func = Counter.new(64, nonce)

        with open(key_filename, 'rb') as keyfile:
            key = keyfile.read()

            decryptor = AES.new(key, AES.MODE_CTR, counter=counter_func)

            with open(out_filename, 'wb') as outfile:
                print(
                    f'{bcolors.BOLD}Decrypting cipher{bcolors.WARNING} '
                    f'{in_filename}{bcolors.ENDC+bcolors.BOLD} ...{bcolors.ENDC}'
                )
                chunksize = 64 * 1024
                start = timeit.default_timer()

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                end = timeit.default_timer()
                print(
                    f'{bcolors.BOLD}Decryption {bcolors.OKGREEN}complete'
                    f'{bcolors.ENDC+bcolors.BOLD}. Time elapsed: {end-start} seconds{bcolors.ENDC}'
                )
