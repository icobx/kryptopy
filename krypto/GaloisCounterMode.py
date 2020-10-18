import os, timeit

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto import Random

from utility.bcolors import bcolors
from utility.validation import get_filename, validate_exists_file


class _GaloisCounterMode:
    CHUNK_SIZE = 64 * 1024
    STYLE = bcolors.OKGREEN+bcolors.BOLD
    END_S = bcolors.ENDC

    def __init__(self):
        pass


    def generate_rsa_key_pair(self, private_keyfile, public_keyfile, pass_phrase=None):
        # private_keyfile - file where private key will be stored
        # keyfile_pub - file where public key will be stored
        key = RSA.generate(2048)

        key_file_priv = get_filename(private_keyfile)
        with open(key_file_priv, 'wb') as priv:
            priv.write(key.export_key(passphrase=pass_phrase))

        key_file_pub = get_filename(public_keyfile)
        with open(key_file_pub, 'wb') as pub:
            pub.write(key.publickey().export_key())

        print(f'New RSA key-pair generated: '
              f'< {self.STYLE}{key_file_priv}{bcolors.ENDC} '
              f'| {self.STYLE}{key_file_pub}{bcolors.ENDC}  >')

    def encrypt_with_rsa(self, in_filename, public_key, out_filename=None):

        with open(public_key, 'rb') as pub:
            pub_key = RSA.import_key(pub.read())

            rsa_cipher = PKCS1_OAEP.new(pub_key)

            infile_enc = rsa_cipher.encrypt(in_filename)

            if not out_filename:
                return infile_enc

            outfile_name = get_filename(out_filename)

            with open(outfile_name, 'wb') as outfile:
                outfile.write(infile_enc)
                print(f'Encrypted message stored in {self.STYLE}{outfile_name}.')

    def decrypt_with_rsa(self, in_filename, private_key, out_filename=None):

        with open(private_key, 'rb') as priv:
            priv_key = RSA.import_key(priv.read())

            rsa_cipher = PKCS1_OAEP.new(priv_key)

            infile_dec = rsa_cipher.decrypt(in_filename)

            if not out_filename:
                return infile_dec

            outfile_name = get_filename(out_filename)

            with open(outfile_name, 'wb') as outfile:
                outfile.write(infile_dec)
                print(f'Decrypted message stored in {self.STYLE}{outfile_name}.')

    # out_file format: [ nonce (12) | sym_key_enc (256) | encrypted_data (len(data)) | tag (16) ]
    def encrypt_file(self, in_filename, public_key, out_filename):
        # create 96 byt nonce for symmetric cipher
        nonce = Random.get_random_bytes(12)
        # create 128 bit key for symmetric cipher
        sym_key = Random.get_random_bytes(16)
        # create symmetric cipher
        cipher = AES.new(sym_key, AES.MODE_GCM, nonce=nonce)
        # encrypt sym_key with asym cipher (RSA)
        sym_key_enc = self.encrypt_with_rsa(sym_key, public_key)

        ad = nonce + sym_key_enc
        cipher.update(ad)   # --> include in tag

        with open(in_filename, 'rb') as infile:
            o_filename = get_filename(out_filename)
            with open(o_filename, 'wb') as outfile:
                print(f'{bcolors.BOLD}Encrypting file {in_filename} ...{bcolors.ENDC}')

                outfile.write(ad)

                start = timeit.default_timer()

                while True:
                    chunk = infile.read(self.CHUNK_SIZE)
                    if len(chunk) == 0:
                        break
                    outfile.write(cipher.encrypt(chunk))

                outfile.write(cipher.digest())

                end = timeit.default_timer()
                print(
                    f'{bcolors.BOLD}Encryption {bcolors.OKGREEN}complete'
                    f'{bcolors.ENDC + bcolors.BOLD}. Time elapsed: {end - start} seconds{bcolors.ENDC}'
                )

    # in_file format: [ nonce (12) | sym_key_enc (256) | encrypted_data (len(data)) | tag (16) ]
    def decrypt_file(self, in_filename, private_key, out_filename):
        with open(in_filename, 'rb+') as infile:
            nonce = infile.read(12)
            sym_key_enc = infile.read(256)

            sym_key = self.decrypt_with_rsa(sym_key_enc, private_key)

            cipher = AES.new(sym_key, AES.MODE_GCM, nonce=nonce)
            cipher.update(nonce + sym_key_enc)

            o_filename = get_filename(out_filename)
            with open(o_filename, 'wb') as outfile:
                print(f'{bcolors.BOLD}Decrypting ciphertext {in_filename} ...{bcolors.ENDC}')

                start = timeit.default_timer()

                # find tag position in file
                infile.seek(-16, os.SEEK_END)
                # read tag
                tag = infile.read()
                # find tag position again
                infile.seek(-16, os.SEEK_END)
                # remove tag from file
                infile.truncate()
                # find encrypted_data position
                infile.seek(268)

                while True:
                    chunk = infile.read(self.CHUNK_SIZE)
                    if len(chunk) == 0:
                        break
                    outfile.write(cipher.decrypt(chunk))

                # write tag back to the end of file in case it needs to be encrypted
                infile.write(tag)

                end = timeit.default_timer()

                try:
                    cipher.verify(tag)  # verify data integrity

                except ValueError as ve:
                    print(f'{bcolors.FAIL + bcolors.BOLD}{ve}. File could have been tampered with.{bcolors.ENDC}')

                    user_input = input(
                        f'Would you like to keep decrypted file anyway? '
                        f'{bcolors.BOLD}(Y/n){bcolors.ENDC}: '
                    )
                    user_input = user_input[0].lower() if len(user_input) else 'y'

                    response = 'File truncated.'
                    if 'y' in user_input:
                        print(f'{bcolors.WARNING + bcolors.BOLD}Keeping unverified file.{bcolors.ENDC}')
                        return
                    elif 'n' not in user_input:
                        response = 'Ambiguous input. ' + response

                    outfile.close()
                    os.remove(o_filename)
                    print(response)
                    return

                print(
                    f'{bcolors.BOLD}Decryption {bcolors.OKGREEN}complete'
                    f'{bcolors.ENDC + bcolors.BOLD}. Time elapsed: {end - start} seconds{bcolors.ENDC}'
                )

    # method for tampering with encrypted file
    def fuck_up_file(self, infile, byte_string=b'\x35', position=268):
        with open(infile, 'rb+') as file:
            file.seek(position)
            file.write(byte_string)
