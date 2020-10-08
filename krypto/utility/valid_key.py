import sys, argparse

from .bcolors import bcolors


def valid_key(keyfile):
    # TODO: fix when keyfile doesn't exist
    with open(keyfile, 'rb') as key_file:
        size = len(key_file.read())

        if size != 16:
            raise argparse.ArgumentTypeError(
                f'{bcolors.FAIL}{keyfile} is not valid key{bcolors.ENDC}'
            )

    return keyfile
