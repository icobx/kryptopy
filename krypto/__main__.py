import timeit

from utility.setup_parser import setup_parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    if not args.mode:
        parser.parse_args(['-h'])
        return

    args.func(args)


# stupid simple performance testing function
# def test():
#     time_data = []
#     mode = _GaloisCounterMode()
#     for i in range(100):
#         start = timeit.default_timer()
#         mode.decrypt_file('1gb_test_enc', 'priv_key', '1gb_test_dec')
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
