import getopt
import sys

# from Crypto.PublicKey import RSA
# from Crypto import Random

from krypto.utility.helper import helper
from krypto.encrypt_file import encrypt_file
from krypto.decrypt_file import decrypt_file


def main():
    argv = sys.argv[1:]

    if len(argv) == 0:
        helper()
        return

    # random_generator = Random.new().read
    # test = RSA.generate(2048, random_generator)
    # msg = 'test RSA key'
    # enc = test.encrypt(msg.encode('utf-8'), 16)
    # # print(test.exportKey())
    # print(enc)
    # test2 = RSA.importKey(test.exportKey())
    # dec = test2.decrypt(enc)
    # print(dec.decode('utf-8'))
    # inputfile = ''
    # outputfile = ''

    # TODO: use optparse
    try:
        opts, args = getopt.getopt(argv, "he:d:k:", ["help", "encrypt=", "decrypt=", "key_file="])  # , "decrypt=", "kfile="
    except getopt.GetoptError:
        print('Help: kryptopy -h ')
        sys.exit(2)

    to_dec = None
    key_file = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helper()
            sys.exit()

        elif opt in ("-e", "--encrypt"):
            encrypt_file(arg)
            sys.exit()

        elif opt in ("-d", "--decrypt"):
            to_dec = arg

        elif opt in ("-k", "--key_file"):
            key_file = arg

    if to_dec and key_file:
        decrypt_file(to_dec, key_file)
    # print('Input file is ', inputfile)
    # print('Output file is ', outputfile)


if __name__ == '__main__':
    main()
