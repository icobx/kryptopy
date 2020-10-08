import argparse, sys

from krypto.encrypt_file import encrypt_file
from krypto.decrypt_file import decrypt_file

from krypto.utility.valid_key import valid_key
from krypto.utility.bcolors import bcolors


def main():
    parser = argparse.ArgumentParser(
        description=f'{bcolors.BOLD}Simple tool for file encryption/decryption.{bcolors.ENDC}'
    )

    parser.add_argument('infile', action='store',
                        help=f'file to be encrypted ( {bcolors.WARNING+bcolors.BOLD}-d: decrypted {bcolors.ENDC})')
    parser.add_argument('keyfile', action='store', type=valid_key,
                        help='encryption key will be stored here '
                             '( if non-existing is provided, new file will be created | '
                             f' {bcolors.WARNING+bcolors.BOLD}-d: existing must be provided{bcolors.ENDC} )')
    parser.add_argument('outfile', action='store',
                        help='encrypted file will be stored here '
                             '( if non-existing is provided, new file will be created )')
    parser.add_argument('-d', '--decrypt', action='store_true',
                        help='decryption mode '
                             f'( {bcolors.WARNING+bcolors.BOLD}valid 128 bit key must be provided{bcolors.ENDC} )')

    args = parser.parse_args()
    print(args)
    parser.print_help()
    # parser.format_help()

    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument('-e', '--encrypt', action='store_true', help="encrypt functionality")
    # group.add_argument('-d', '--decrypt', action='store_true', help="decrypt functionality")
    # # print(("-d" in sys.argv or "--decrypt" in sys.argv))
    # # print(sys.argv)
    # decrypt_req = "-d" in sys.argv or "--decrypt" in sys.argv
    # parser.add_argument('-i', '--infile', metavar='', required=True, help="Input file")
    # parser.add_argument('-k', '--keyfile', metavar='',
    #                     required=("-d" in sys.argv or "--decrypt" in sys.argv), help="Key file")
    # parser.add_argument('-o', '--outfile', metavar='', help="Output file", )
    #
    # args = parser.parse_args()
    #
    # if args.encrypt:
    #     if args.outfile:
    #         encrypt_file(args.infile, args.keyfile, args.outfile)
    #     else:
    #         encrypt_file(args.infile, args.keyfile)
    # elif args.decrypt:
    #     if args.outfile:
    #         decrypt_file(args.keyfile, args.infile, args.outfile)
    #     else:
    #         decrypt_file(args.keyfile, args.infile)


if __name__ == '__main__':
    main()
