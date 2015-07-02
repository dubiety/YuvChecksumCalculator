#!/usr/bin/env python

import io
import os.path as path
import sys
sys.path.append(path.abspath(path.join(path.abspath(__file__), '..', '..')))
from ChecksumCalculator import arg_parse, arg_parser, ChecksumCalculator

def main():
    import cProfile
    import pstats

    pr = cProfile.Profile()
    pr.enable()
    #  Start profiling
    args = arg_parse(arg_parser(), '-i ..\\big_buck_bunny_360p24.y4m -o haha.md5 -r 1920 1080 -n 100'.split(' '))
    checksum_calculator = ChecksumCalculator(args)
    checksum_calculator.calculate()

    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(15)
    print(s.getvalue())
    return 0

if __name__ == '__main__':
    exit(main())
