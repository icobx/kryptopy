import argparse, timeit

from krypto.encrypt_file import encrypt_file
from krypto.decrypt_file import decrypt_file

from utility.validation import valid_key, validate_infile
from utility.bcolors import bcolors


def main():
    parser = argparse.ArgumentParser(
        description=f'{bcolors.BOLD}Simple tool for file encryption/decryption.{bcolors.ENDC}'
    )

    parser.add_argument('infile', action='store',
                        help=f'file to be encrypted ( {bcolors.WARNING + bcolors.BOLD}-d: decrypted{bcolors.ENDC} )')
    parser.add_argument('keyfile', action='store',
                        help='encryption key will be stored here '
                             '( if non-existing is provided, new file will be created | '
                             f' {bcolors.WARNING + bcolors.BOLD}-d: existing must be provided{bcolors.ENDC} )')
    parser.add_argument('outfile', action='store',
                        help='encrypted file will be stored here '
                             '( if non-existing is provided, new file will be created |'
                             f' {bcolors.WARNING + bcolors.BOLD}-d: decrypted{bcolors.ENDC} )')
    parser.add_argument('-d', '--decrypt', action='store_true', default=False,
                        help='decryption mode '
                             f'( {bcolors.WARNING + bcolors.BOLD}valid 128 bit key must be provided{bcolors.ENDC} )')

    args = parser.parse_args()

    validate_infile(args.infile)

    if args.decrypt and valid_key(args.keyfile):
        decrypt_file(args.infile, args.keyfile, args.outfile)
        return

    encrypt_file(args.infile, args.keyfile, args.outfile)


# def test():
#     time_data = []
#     for i in range(100):
#         start = timeit.default_timer()
#         decrypt_file('/Users/icobx/Documents/upb/zadanie2/kryptopy/tf_1b_enc', '/Users/icobx/Documents/upb/zadanie2/kryptopy/tkf', '/Users/icobx/Documents/upb/zadanie2/kryptopy/tf_1b_dec')
#         end = timeit.default_timer()
#         time_data.append(end - start)
#
#     sum = 0
#     for n in time_data:
#         sum += n
#
#     print(sum / len(time_data))


if __name__ == '__main__':
    main()
