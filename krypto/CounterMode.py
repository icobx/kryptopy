import timeit

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter

from utility.bcolors import bcolors
from utility.validation import get_filename, validate_exists_file


class CounterMode:
    def __init__(self):
        pass

    def test(self):
        print('test')

    def encrypt_file(self, in_filename, key_file, out_filename):
        validate_exists_file(in_filename)

        # generate random 128 bit key
        key = Random.get_random_bytes(16)
        # random nonce (equivalent to IV) of length 64 bit, will be packed with enc msg
        nonce = Random.get_random_bytes(8)
        # Counter.new() creates counter function for AES in CTR mode to call and increment counter, nonce is prefix
        counter_func = Counter.new(64, nonce)

        encryptor = AES.new(key, AES.MODE_CTR, counter=counter_func)

        with open(in_filename, 'rb') as infile:

            o_file = get_filename(out_filename)
            with open(o_file, 'wb') as outfile:
                print(
                    f'{bcolors.BOLD}Encrypting file{bcolors.WARNING} '
                    f'{in_filename}{bcolors.ENDC + bcolors.BOLD} ...{bcolors.ENDC}'
                )
                chunksize = 64 * 1024

                start = timeit.default_timer()
                # 8 bytes, write into outfile unencrypted
                outfile.write(nonce)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(encryptor.encrypt(chunk))

                k_file = get_filename(key_file)
                with open(k_file, 'wb') as keyfile:
                    keyfile.write(key)

                    end = timeit.default_timer()
                    print(
                        f'{bcolors.BOLD}Decryption {bcolors.OKGREEN}complete'
                        f'{bcolors.ENDC + bcolors.BOLD}. Time elapsed: {end - start} seconds{bcolors.ENDC}'
                    )

    def decrypt_file(self, in_filename, key_filename, out_filename):
        with open(in_filename, 'rb') as infile:
            # nonce was added unencrypted at the beginning, sizeof(8 bytes)
            nonce = infile.read(8)
            counter_func = Counter.new(64, nonce)

            with open(key_filename, 'rb') as keyfile:
                key = keyfile.read()
                decryptor = AES.new(key, AES.MODE_CTR, counter=counter_func)

                o_file = get_filename(out_filename)
                with open(o_file, 'wb') as outfile:
                    print(
                        f'{bcolors.BOLD}Decrypting cipher{bcolors.WARNING} '
                        f'{in_filename}{bcolors.ENDC + bcolors.BOLD} ...{bcolors.ENDC}'
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
                        f'{bcolors.ENDC + bcolors.BOLD}. Time elapsed: {end - start} seconds{bcolors.ENDC}'
                    )
