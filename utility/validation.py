import os, argparse

from .bcolors import bcolors

style = bcolors.FAIL + bcolors.UNDERLINE


def valid_key(keyfile):
    try:
        if os.path.isdir(keyfile):
            raise argparse.ArgumentTypeError(
                f'{style}{keyfile} is directory but must be file{bcolors.ENDC}'
            )

        status = os.stat(keyfile)
        if status.st_size != 16:
            raise argparse.ArgumentTypeError(
                f'{style}{keyfile} is not valid key{bcolors.ENDC}'
            )
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(
            f'{style}{keyfile} was not found{bcolors.ENDC}'
        )

    return True


def validate_infile(infile):
    if not os.path.exists(infile):
        raise argparse.ArgumentTypeError(
            f'{style}{infile} does not exist{bcolors.ENDC}'
        )

    elif os.path.isdir(infile):
        raise argparse.ArgumentTypeError(
            f'{style}{infile} is directory but must be file{bcolors.ENDC}'
        )


def get_filename(file):
    # if not file:
    #     return None

    path = os.path.expanduser(file)

    if not os.path.exists(path):
        return path

    root, ext = os.path.splitext(os.path.expanduser(path))
    fdir = os.path.dirname(root)
    if not fdir:
        fdir = './'

    fname = os.path.basename(root)
    candidate = fname + ext
    index = 0
    ls = set(os.listdir(fdir))

    while candidate in ls:
        candidate = "{}_{}{}".format(fname, index, ext)
        index += 1

    return os.path.join(fdir, candidate)
