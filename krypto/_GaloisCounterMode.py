import os, csv, timeit

from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto import Random

from utility.bcolors import bcolors
from utility.validation import get_filename


class _GaloisCounterMode:
    def __init__(self):
        pass

    def test(self):
        print('test_gcm')

    def generate_rsa_key(self, private_keyfile, keyfile_pub, pass_phrase=None, size=2048):
        # private_keyfile - file where private key will be stored
        # keyfile_pub - file where public key will be stored

        key = RSA.generate(size)

        key_file_priv = get_filename(private_keyfile)
        with open(key_file_priv, 'wb') as priv:
            priv.write(key.export_key(passphrase=pass_phrase))

        key_file_pub = get_filename(keyfile_pub)
        with open(key_file_pub, 'wb') as pub:
            pub.write(key.publickey().exportKey())

    def encrypt_with_rsa(self, public_key, symmetric_key, symmetric_key_enc=None):
        with open(public_key, 'rb') as pub:

            pub_key = RSA.import_key(pub.read())

            rsa_cipher = PKCS1_OAEP.new(pub_key)

            sym_key_enc = rsa_cipher.encrypt(symmetric_key)
            print(len(sym_key_enc))

            if not symmetric_key_enc:
                return sym_key_enc

            # keby chcem ten kluc do file-u
            # with open(symmetric_key, 'rb') as sym: sym.read()
            # only temp for checking

    def decrypt_with_rsa(self, private_key, encrypted_sym_key, symmetric_key_dec=None):
        with open(private_key, 'rb') as priv:
            test1 = priv.read()
            print(test1, '\n')
            print(len(encrypted_sym_key))
            priv_key = RSA.import_key(test1) #priv.read()

            rsa_cipher = PKCS1_OAEP.new(priv_key)

            if not symmetric_key_dec:
                return rsa_cipher.decrypt(encrypted_sym_key)

            # with open(encrypted_sym_key, 'rb') as e_sym:
            #     enc_sym_key = e_sym.read()
            #
            #     rsa_cipher = PKCS1_OAEP.new(priv_key)
            #
            #     sym_key = rsa_cipher.decrypt(enc_sym_key)
            #
            #     return sym_key

    # out_file format: [ nonce (12) | sym_key_enc (256) | encrypted_data (sizeof(data)) | tag (16) ]
    def encrypt_file(self, public_key, in_filename, out_filename):
        # create 128 bit key for symmetric cipher
        sym_key = Random.get_random_bytes(16)
        # create 96 byt nonce for symmetric cipher
        nonce = Random.get_random_bytes(12)
        # create symmetric cipher
        cipher = AES.new(sym_key, AES.MODE_GCM, nonce=nonce)
        # encrypt sym_key with asym cipher (RSA)
        sym_key_enc = self.encrypt_with_rsa(public_key, sym_key)
        # vytvor header = [nonce, zasifrovany key]
        # auth_data = nonce + sym_key_enc
        # cipher.update(auth_data)
        cipher.update(nonce + sym_key_enc)
        # zasifruj data
        with open(in_filename, 'rb') as infile:
            o_filename = get_filename(out_filename)
            with open(o_filename, 'wb') as outfile:
                print(
                    f'{bcolors.BOLD}Encrypting file{bcolors.WARNING} '
                    f'{in_filename}{bcolors.ENDC + bcolors.BOLD} ...{bcolors.ENDC}'
                )
                # csv_writer = csv.writer(outfile)
                #
                # row = [b64encode(nonce).decode('utf-8'), b64encode(sym_key_enc).decode('utf-8'), None, None]
                # csv_writer.writerow(row)
                outfile.write(nonce)
                outfile.write(sym_key_enc)
                # vypis
                chunk_size = 64 * 1024

                # outfile.write()
                start = timeit.default_timer()
                while True:
                    chunk = infile.read(chunk_size)
                    if len(chunk) == 0:
                        break

                    outfile.write(cipher.encrypt(chunk))
                    # row = [None, None, b64encode(cipher.encrypt(chunk)).decode('utf-8'), None]
                    # csv_writer.writerow(row)

                outfile.write(cipher.digest())

                end = timeit.default_timer()
                print(
                    f'{bcolors.BOLD}Decryption {bcolors.OKGREEN}complete'
                    f'{bcolors.ENDC + bcolors.BOLD}. Time elapsed: {end - start} seconds{bcolors.ENDC}'
                )
            #vypis

    def decrypt_file(self, private_key, in_filename, out_filename):

        with open(in_filename, 'rb+') as infile:
            nonce = infile.read(12)
            sym_key_enc = infile.read(256)

            sym_key = self.decrypt_with_rsa(private_key, sym_key_enc)

            cipher = AES.new(sym_key, AES.MODE_GCM, nonce=nonce)
            cipher.update(nonce + sym_key_enc)

            o_filename = get_filename(out_filename)
            with open(o_filename, 'wb') as outfile:
                print(
                    f'{bcolors.BOLD}Decrypting cipher{bcolors.WARNING} '
                    f'{in_filename}{bcolors.ENDC + bcolors.BOLD} ...{bcolors.ENDC}'
                )
                chunk_size = 64 * 1024
                start = timeit.default_timer()

                infile.seek(-16, os.SEEK_END)
                tag = infile.read()
                infile.seek(-16, os.SEEK_END)
                infile.truncate()
                infile.seek(268)

                while True:
                    chunk = infile.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    outfile.write(cipher.decrypt(chunk))
                infile.write(tag)
                try:
                    cipher.verify(tag)
                except ValueError as ve:
                    print(ve)
                    return

                end = timeit.default_timer()
                print(
                    f'{bcolors.BOLD}Decryption {bcolors.OKGREEN}complete'
                    f'{bcolors.ENDC + bcolors.BOLD}. Time elapsed: {end - start} seconds{bcolors.ENDC}'
                )
        #     outfile.seek(-16, os.SEEK_END)

    def fuck_up_file(self, infile):
        with open(infile, 'rb+') as file:
            file.seek(269)
            c = file.read(1)
            print(c)
            c = b'\x35'
            file.seek(-1, 1)
            file.write(c)
            file.seek(-1, 1)
            print(file.read(1))
            file.close()
