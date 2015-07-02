#!/usr/bin/python
#
#  Copyright (c) 2015 YUV Checksum calculator authors. All Rights Reserved.
#
#  Use of this source code is governed by a GPL v2 license
#  that can be found in the LICENSE file in the root of the source tree.
#

from sys import exit, argv
import argparse
import hashlib
import logging
log = logging.getLogger(__name__)


class ChecksumCalculator(object):
    """Class ChecksumCalculator
    Calculate checksum of a YUV file.
    Support format: IYUV or monochrome Y data

    Init: Enter a dictionary with required key value (See argument)
    Calculation: call member function calculate()
    """

    def __init__(self, args):
        self.input_file = args.input_file
        self.output_file = args.output_file
        self.start = args.start
        self.frames_to_calculate = args.frames_to_calculate
        self.is_mono = args.is_mono
        self.combine_calculate = args.combine_calculate
        self.use_md5 = args.use_md5
        self.use_sha1 = args.use_sha1
        self.width, self.height = args.resolution
        self.luma_size = self.width * self.height
        self.chroma_size = 0 if self.is_mono else self.luma_size >> 2
        if self.use_md5:
            self.checksum_func = hashlib.md5
        else:
            self.checksum_func = hashlib.sha1

    def calculate(self):
        # frame_left = self.frames_to_calculate
        frame_count = 1
        skip_byte = (self.luma_size + self.chroma_size) * self.start

        # Start calculation frame by frame and save to output file
        print("Calculating....")
        self.input_file.seek(skip_byte)
        chunk = self.input_file.read(self.luma_size)
        while chunk and frame_count <= self.frames_to_calculate:
            # Log frame number
            frame_num_str = "[" + str(frame_count) + "] "
            # Luma part
            checksum = self.checksum_func()
            checksum.update(chunk)
            if not self.combine_calculate:
                self.output_file.write(checksum.hexdigest() + '\n')
                log.debug(frame_num_str + "Y " + checksum.hexdigest())

            # Chroma part
            if not self.is_mono:
                channel = 0
                while channel < 2:
                    chunk = self.input_file.read(self.chroma_size)
                    if not self.combine_calculate:
                        checksum = self.checksum_func()
                    checksum.update(chunk)
                    if not self.combine_calculate:
                        self.output_file.write(checksum.hexdigest() + '\n')
                        log.debug(frame_num_str + ("U " if channel == 0 else "V ") + checksum.hexdigest())
                    channel += 1
                if self.combine_calculate:
                    self.output_file.write(checksum.hexdigest() + '\n')
                    log.debug(frame_num_str + checksum.hexdigest())

            chunk = self.input_file.read(self.luma_size)
            # frame_left -= 1
            frame_count += 1

        print("Done! {frames} calculated at file {file_name}".format(frames=self.frames_to_calculate,
                                                                     file_name=self.output_file.name))
        return 0


def get_version():
    """Return this module version"""
    return '%(prog)s ' + 'v0.1 alpha'

def arg_parser():
    parser = argparse.ArgumentParser(description='Calculate IYUV MD5 or SHA', prog='YUV Checksum Calculator')
    parser.add_argument('-v', '--version', action='version', version=get_version())
    parser.add_argument('-i', '--input', type=argparse.FileType('rb'), dest='input_file', required=True,
                        metavar='<file name>',
                        help='YUV input file name.')
    parser.add_argument('-o', '--output', type=argparse.FileType('wt'), dest='output_file', default='out.checksum',
                        metavar='<file name>',
                        help='Checksum output file name (text file).')
    parser.add_argument('-r', '--res', type=int, nargs=2, dest='resolution', required=True,
                        metavar=('<W>', '<H>'),
                        help='Image resolution (Width, Height).')
    parser.add_argument('-s', '--start', type=int, dest='start',
                        metavar='<N>', default=0,
                        help='N means frame start index (start from 0).')
    parser.add_argument('-n', '--frames', type=int, nargs='?', dest='frames_to_calculate', default=0,
                        metavar='<frame count>',
                        help='Total frame number need to be calculated. No arg means calculate till EOF.')
    parser.add_argument('-m', '--mono', dest='is_mono', action='store_true', default=False,
                        help='Specify input file is monochrome YUV file.')
    parser.add_argument('-c', '--combine', dest='combine_calculate', action='store_true',
                        help='Only calculate one MD5 for YUV 3 channel combined.')
    # parser.add_argument('-p', '--rpadding', type=int, default=0, nargs=1, dest='rpadding',
    # metavar='<padding>', help='YUV right padding (in pixels). e.g. To skip 16 pixel data, enter \"-p 16\"')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--md5', dest='use_md5', action='store_true',
                       help='Calculate MD5 checksum (default is true).')
    group.add_argument('--sha1', dest='use_sha1', action='store_true',
                       help='Calculate SHA1 instead of MD5.')
    # parser.print_help()

    return parser

def arg_parse(parser, _argv):
    args = parser.parse_args(_argv)
    if not args.use_sha1:
        args.use_md5 = True
    # print(args)
    return args

def main():
    # Setup logging information
    formatter = logging.Formatter('%(message)s')
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    log.addHandler(console)
    log.setLevel(logging.WARNING)  # Change debug level here

    args = arg_parse(arg_parser(), argv[1:])
    checksum_calculator = ChecksumCalculator(args)
    exit_status = checksum_calculator.calculate()
    return exit_status

if __name__ == '__main__':
    exit(main())
