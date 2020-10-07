import timeit

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Util import Counter

from kryptopy.utility.bcolors import bcolors


def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    # random nonce (equivalent to IV) of length 64 bit, will be packed with enc msg
    nonce = Random.get_random_bytes(8)
    # Counter.new() creates counter function for AES in CTR mode to call and increment counter, nonce is prefix
    counter_func = Counter.new(64, nonce)

    # encode key to utf-8, hash and slice it to fit 16 bytes
    hashed_key_16 = SHA256.new(key.encode('utf-8')).hexdigest()[:16]  # -> mame generovat nahodny key

    encryptor = AES.new(hashed_key_16, AES.MODE_CTR, counter=counter_func)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            print(
                f'{bcolors.BOLD}Encrypting file{bcolors.WARNING} '
                f'{in_filename}{bcolors.ENDC + bcolors.BOLD} ...{bcolors.ENDC}'
            )
            start = timeit.default_timer()
            # 8 bytes, write into outfile unencrypted
            outfile.write(nonce)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break

                outfile.write(encryptor.encrypt(chunk))

            end = timeit.default_timer()
            print(
                f'{bcolors.BOLD}Decryption {bcolors.OKGREEN}complete'
                f'{bcolors.ENDC + bcolors.BOLD}. Time elapsed: {end - start} seconds{bcolors.ENDC}'
            )