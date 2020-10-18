import argparse

from utility.bcolors import bcolors
from utility.validation import validate_sym_key, validate_exists_file

from krypto.GaloisCounterMode import GaloisCounterMode
from krypto.CounterMode import CounterMode


def am_default(args):
    try:
        validate_exists_file(args.infile, args.keyfile)

        mode = GaloisCounterMode()

        if args.decrypt:
            mode.decrypt_with_rsa(args.infile, args.keyfile, args.outfile)
            return

        mode.encrypt_with_rsa(args.infile, args.keyfile, args.outfile)

    except TypeError as te:
        print(f'{bcolors.FAIL + bcolors.BOLD}<{args.keyfile}>: {te}{bcolors.ENDC}')

    except Exception as e:
        print(f'{bcolors.FAIL + bcolors.BOLD}{e}{bcolors.ENDC}')


def gc_default(args):
    try:
        validate_exists_file(args.infile, args.keyfile)

        mode = GaloisCounterMode()

        if args.decrypt:
            mode.decrypt_file(args.infile, args.keyfile, args.outfile)
            return

        mode.encrypt_file(args.infile, args.keyfile, args.outfile)

    except TypeError as te:
        print(f'{bcolors.FAIL + bcolors.BOLD}<{args.keyfile}>: {te}{bcolors.ENDC}')

    except Exception as e:
        print(f'{bcolors.FAIL + bcolors.BOLD}{e}{bcolors.ENDC}')


def sm_default(args):
    try:
        validate_exists_file(args.infile)
    except argparse.ArgumentTypeError as ate:
        print(ate)
        return

    mode = CounterMode()

    if args.decrypt:
        try:
            validate_exists_file(args.keyfile)
            validate_sym_key(args.keyfile)
        except FileNotFoundError or IsADirectoryError or argparse.ArgumentTypeError as e:
            if type(e) is FileNotFoundError:
                print(
                    f'{bcolors.FAIL + bcolors.BOLD}<{e.filename}>: no such file{bcolors.ENDC}'
                )
            else:
                print(f'{bcolors.FAIL + bcolors.BOLD}{e}{bcolors.ENDC}')
            return

        mode.decrypt_file(args.infile, args.keyfile, args.outfile)
        return

    mode.encrypt_file(args.infile, args.keyfile, args.outfile)


def gn_default(args):
    mode = GaloisCounterMode()

    mode.generate_rsa_key_pair(args.private_key, args.public_key, args.passphrase)


def setup_parser():
    warning = bcolors.WARNING + bcolors.BOLD
    ends = bcolors.ENDC

    description = f'{bcolors.BOLD}Simple tool for file encryption/decryption.{bcolors.ENDC}'

    parser = argparse.ArgumentParser(description=description)

    modes = parser.add_subparsers(title='modes',
                                  help=f'followed by {warning}-h, --help{ends} to show help for given mode',
                                  dest='mode')
    # gcm mode
    parser_hybrid = modes.add_parser('g', help='AES-GCM hybrid encryption / decryption mode')

    parser_hybrid.add_argument('infile', action='store',
                               help=f'file to be encrypted '
                                    f'( {warning}-d: decrypted{ends} )')

    parser_hybrid.add_argument('keyfile', action='store',
                               help=f'public key for encryption of symmetric cipher key'
                                    f' ( {warning}-d: private key for decryption{ends} )')

    parser_hybrid.add_argument('outfile', action='store', nargs='?', default='hybrid_outfile',
                               help='encrypted data will be stored here, '
                                    'if non-existing is provided, new file will be created '
                                    '( default: hybrid_outfile, '
                                    f' {warning}-d: decrypted{ends} )')

    parser_hybrid.add_argument('-d', '--decrypt', action='store_true', default=False,
                               help='decryption mode')
    parser_hybrid.set_defaults(func=gc_default)

    # asymmetric RSA mode
    parser_asym = modes.add_parser('a', help='asymmetric PKCS1_OAEP encryption / decryption mode')
    parser_asym.add_argument('infile', action='store',
                             help=f'message to be encrypted '
                                  f'( {warning}-d: decrypted{ends} )')

    parser_asym.add_argument('keyfile', action='store',
                             help=f'public key for encryption of message'
                                  f'( {warning}-d: private key for decryption{ends} )')

    parser_asym.add_argument('outfile', action='store', nargs='?', default='asymmetric_outfile',
                             help='encrypted message will be stored here, '
                                  'if non-existing is provided, new file will be created '
                                  '( default: asymmetric_outfile, '
                                  f' {warning}-d: decrypted{ends} )')

    parser_asym.add_argument('-d', '--decrypt', action='store_true', default=False,
                             help='decryption mode')
    parser_asym.set_defaults(func=am_default)

    # symmetric CTR mode
    parser_sym = modes.add_parser('s', help='AES-CTR symmetric encryption / decryption mode')
    parser_sym.add_argument('infile', action='store',
                            help=f'file to be encrypted '
                                 f'( {warning}-d: decrypted{ends} )')

    parser_sym.add_argument('keyfile', action='store',
                            help=f'key for encrypted file will be store here'
                                 f'( {warning}-d: key for decryption will be read from here{ends} )')

    parser_sym.add_argument('outfile', action='store', nargs='?', default='symmetric_outfile',
                            help='encrypted data will be stored here, '
                                 'if non-existing is provided, new file will be created '
                                 '( default: symmetric_outfile, '
                                 f' {warning}-d: decrypted{ends} )')

    parser_sym.add_argument('-d', '--decrypt', action='store_true', default=False,
                            help='decryption mode'
                                 f'( {warning}keyfile: valid 128 bit key must be provided{ends} )')
    parser_sym.set_defaults(func=sm_default)

    # generate rsa key-pair mode
    parser_gen = modes.add_parser('gen', help='mode for generating RSA key-pair')
    parser_gen.add_argument('public_key', action='store',
                            help='public key will be store here')
    parser_gen.add_argument('private_key', action='store',
                            help='private key will be store here')
    # add this in future?
    # parser_gen.add_argument('-p', '--passphrase', action='store',
    #                       help='pass-phrase for private key')
    parser_gen.set_defaults(func=gn_default)

    return parser

    # old code, kept here just in case
 ######################################################################################################################

    # positional params
    # parser.add_argument('infile', action='store',
    #                     help=f'file to be encrypted ( {bcolors.WARNING + bcolors.BOLD}-d: decrypted{bcolors.ENDC} )')
    # parser.add_argument('keyfile', action='store',
    #                     help='encryption key will be stored here, '
    #                          'if non-existing is provided, new file will be created '
    #                          f'( {bcolors.WARNING + bcolors.BOLD}-d: existing must be provided{bcolors.ENDC} )')
    #
    # # optional positional (output)
    # parser.add_argument('outfile', action='store', nargs='?', default='kryptopy_outfile',
    #                     help='encrypted file will be stored here, '
    #                          'if non-existing is provided, new file will be created '
    #                          '( default: kryptopy_outfile |'
    #                          f' {bcolors.WARNING + bcolors.BOLD}-d: decrypted{bcolors.ENDC} )')
    #
    # # optional params
    # parser.add_argument('-d', '--decrypt', action='store_true', default=False,
    #                     help='decryption mode '
    #                          f'( {bcolors.WARNING + bcolors.BOLD}valid 128 bit key must be provided{bcolors.ENDC} )')
    #
    # # mutually exclusive opt params
    # modes_group = parser.add_mutually_exclusive_group()
    # modes_group.add_argument('-a', '--asymmetric', action='store_true', default=False,
    #                     help=f'asymmetric encryption ( {bcolors.WARNING + bcolors.BOLD}'
    #                          f'with -d: decryption{bcolors.ENDC} ) mode, only for short messages')
    #
    # # gen_group = modes_group.add_argument_group()
    # modes_group.add_argument('-g', '--generate', action='store_true', default=False,
    #                     help='generates RSA key-pair, '
    #                          'requires filenames for both private and public key:'
    #                          f' {bcolors.WARNING + bcolors.BOLD}private_keyfile -> infile |'
    #                          f' public_keyfile -> keyfile {bcolors.ENDC}')
    # # gen_group.add_argument('-p', '-pass', action='store', help='test test')
    #
    # # old mode
    # modes_group.add_argument('-C', '--Counter', action='store_true', default=False,
    #                     help='AES-CTR mode without integrity validation and asymmetric encryption.')
    #
    # args = parser.parse_args()
    #
    # if args.Counter:
    #     try:
    #         validate_exists_file(args.infile, args.keyfile)
    #     except argparse.ArgumentTypeError as ate:
    #         print(ate)
    #         return
    #
    #     mode = _CounterMode()
    #
    #     if args.decrypt:
    #         try:
    #             validate_sym_key(args.keyfile)
    #         except FileNotFoundError or IsADirectoryError or argparse.ArgumentTypeError as e:
    #             if type(e) is FileNotFoundError:
    #                 print(
    #                     f'{bcolors.FAIL+bcolors.BOLD}<{e.filename}>: no such file{bcolors.ENDC}'
    #                 )
    #             else:
    #                 print(e.strerror)
    #             return
    #
    #         mode.decrypt_file(args.infile, args.keyfile, args.outfile)
    #         return
    #
    #     mode.encrypt_file(args.infile, args.keyfile, args.outfile)
    #
    # else:
    #     mode = _GaloisCounterMode()
    #
    #     if args.generate:
    #         mode.generate_rsa_key_pair(args.infile, args.keyfile)
    #
    #     else:
    #         try:
    #             validate_exists_file(args.infile, args.keyfile)
    #         except argparse.ArgumentTypeError as ate:
    #             print(ate)
    #             return
    #
    #         try:
    #             if args.asymmetric:
    #                 if args.decrypt:
    #                     mode.decrypt_with_rsa(args.infile, args.keyfile, args.outfile)
    #                 else:
    #                     mode.encrypt_with_rsa(args.infile, args.keyfile, args.outfile)
    #                 return
    #
    #             if args.decrypt:
    #                 mode.decrypt_file(args.infile, args.keyfile, args.outfile)
    #                 return
    #
    #             mode.encrypt_file(args.infile, args.keyfile, args.outfile)
    #         except ValueError or IndexError or TypeError as e:
    #             print(f'{bcolors.FAIL+bcolors.BOLD}{e}{bcolors.ENDC}')


     ##############################################################################################################################