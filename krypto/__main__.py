import argparse, timeit

from krypto.encrypt_file import encrypt_file
from krypto.decrypt_file import decrypt_file
from krypto._CounterMode import _CounterMode
from krypto._GaloisCounterMode import _GaloisCounterMode

from utility.validation import valid_key, validate_infile
from utility.bcolors import bcolors


def main():
    parser = argparse.ArgumentParser(
        description=f'{bcolors.BOLD}Simple tool for file encryption/decryption.{bcolors.ENDC}'
    )

    # ctr = _CounterMode()
    # test_gcm = _GaloisCounterMode()
    # test_gcm.encrypt_file('pub_key', 'test.txt', 'test.txt.enc')
    # test_gcm.fuck_up_file('test.txt.enc')
    # test_gcm.decrypt_file('priv_key', 'test.txt.enc', 'test.dec.txt')
    # test_gcm.fuck_up_file('test.txt.enc')

    # test_gcm.generate_rsa_key('priv_key', 'pub_key')
    # print(test_ctr.test())
    # print(test_gcm.test())

    # test_gcm.encrypt_with_rsa('pub_key')
    # test_gcm.decrypt_with_rsa('priv_key', 'test_sym_enc')


    # # TODO: add option for old CTR mode
    # positional params
    parser.add_argument('infile', action='store',
                        help=f'file to be encrypted ( {bcolors.WARNING + bcolors.BOLD}-d: decrypted{bcolors.ENDC} )')
    parser.add_argument('keyfile', action='store',
                        help='encryption key will be stored here, '
                             'if non-existing is provided, new file will be created '
                             f'( {bcolors.WARNING + bcolors.BOLD}-d: existing must be provided{bcolors.ENDC} )')

    # optional positional (output)
    parser.add_argument('outfile', action='store', nargs='?', default='kryptopy_outfile',
                        help='encrypted file will be stored here, '
                             'if non-existing is provided, new file will be created '
                             '( default: kryptopy_outfile |'
                             f' {bcolors.WARNING + bcolors.BOLD}-d: decrypted{bcolors.ENDC} )')

    # optional params
    parser.add_argument('-d', '--decrypt', action='store_true', default=False,
                        help='decryption mode '
                             f'( {bcolors.WARNING + bcolors.BOLD}valid 128 bit key must be provided{bcolors.ENDC} )')

    # mutually exclusive opt params
    modes_group = parser.add_mutually_exclusive_group()
    modes_group.add_argument('-a', '--asymmetric', action='store_true', default=False,
                        help=f'asymmetric encryption ( {bcolors.WARNING + bcolors.BOLD}'
                             f'with -d: decryption{bcolors.ENDC} ) mode, only for short messages')

    # gen_group = modes_group.add_argument_group()
    modes_group.add_argument('-g', '--generate', action='store_true', default=False,
                        help='generates RSA key-pair, '
                             'requires filenames for both private and public key:'
                             f' {bcolors.WARNING + bcolors.BOLD}private_keyfile -> infile |'
                             f' public_keyfile -> keyfile {bcolors.ENDC}')
    # gen_group.add_argument('-p', '-pass', action='store', help='test test')

    # old mode
    modes_group.add_argument('-C', '--Counter', action='store_true', default=False,
                        help='AES-CTR mode without integrity validation and asymmetric encryption.')

    # todo: move validations to methods that need them
    print(parser.print_help())

    # todo: uncomment, only commented because was not tested
    # args = parser.parse_args()
    # if args.Counter:
    #     validate_infile(args.infile)
    #     mode = _CounterMode()
    #
    #     if args.decrypt and valid_key(args.keyfile):
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
    #         validate_infile(args.infile)
    #
    #         if args.asymmetric:
    #             if args.decrypt:
    #                 mode.decrypt_with_rsa(args.infile, args.keyfile, args.outfile)
    #             else:
    #                 mode.encrypt_with_rsa(args.infile, args.keyfile, args.outfile)
    #             return
    #
    #         if args.decrypt:
    #             mode.decrypt_file(args.infile, args.keyfile, args.outfile)
    #             return
    #
    #         mode.encrypt_file(args.infile, args.keyfile, args.outfile)



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
