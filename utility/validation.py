import os, argparse

from .bcolors import bcolors

style = bcolors.FAIL + bcolors.BOLD


def validate_sym_key(keyfile):
    # if os.path.isdir(keyfile):
    #     raise IsADirectoryError(
    #         f'{style}<{keyfile}>: is directory but must be file: {bcolors.ENDC}'
    #     )

    status = os.stat(keyfile)
    if status.st_size != 16:
        raise argparse.ArgumentTypeError(
            f'{style}<{keyfile}>: is not valid key{bcolors.ENDC}'
        )
        # print(f'{style}<{fnfe.filename}>: no such file{bcolors.ENDC}')

# def validate_rsa_key(keyfile):



def validate_exists_file(*args):
    for infile in args:
        if not os.path.exists(infile):
            raise FileNotFoundError(
                f'{style}<{infile}>: no such file{bcolors.ENDC}'
            )

        elif os.path.isdir(infile):
            raise IsADirectoryError(
                f'{style}<{infile}>: is directory but must be file{bcolors.ENDC}'
            )

# from stack overflow
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
