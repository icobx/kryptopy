import getopt
import sys

from encrypt_file import encrypt_file
from .utility.helper import helper


def main():
    argv = sys.argv[1:]

    if len(argv) == 0:
        helper()
        return

    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('Help: kryptopy -h ')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            helper()
            sys.exit()

        elif opt in ("-e", "--encrypt"):
            encrypt_file(arg)

        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print('Input file is ', inputfile)
    print('Output file is ', outputfile)


if __name__ == '__main__':
    main()
