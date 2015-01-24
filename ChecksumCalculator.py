#!/usr/bin/python
##
##  Copyright (c) 2014 The WebM project authors. All Rights Reserved.
##
##  Use of this source code is governed by a BSD-style license
##  that can be found in the LICENSE file in the root of the source
##  tree. An additional intellectual property rights grant can be found
##  in the file PATENTS.  All contributing project authors may
##  be found in the AUTHORS file in the root of the source tree.
##

import sys
import argparse

def GetVersion():
  """Return this module version"""
  return '%(prog)s '+'v0.1'

def argParse():
    parser = argparse.ArgumentParser(description='Calculate IYUV MD5/CRC/SHA', prog='YUV Checksum Calculator')
    parser.add_argument('-v', '--version', action='version', version=GetVersion())
    parser.add_argument('-f', '--file', type=argparse.FileType('rb'), nargs=1, dest='input_file', required=True, 
                        metavar='<file name>',
                        help='YUV file name.')
    parser.add_argument('-r', '--res', type=int, nargs=2, dest='resolution', required=True, 
                        metavar=('<W>','<H>'),
                        help='Image resolution (Width, Height).')
    parser.add_argument('-s', '--start', type=int, nargs=1, dest='start',
                        metavar='<N>', default=0,
                        help='N means frame start index (start from 0).')
    parser.add_argument('-n', '--frames', type=int, nargs='?', dest='frames_to_calculate', 
                        metavar='<frame count>',
                        help='Total frame number need to be calculated. No arg means calculate till EOF.')
    parser.add_argument('-m', '--mono', dest='is_mono', action='store_true', default=False,
                        help='Specify input file is monochrome YUV file.')
    parser.add_argument('-c', '--combine', dest='combine_calculate', action='store_true',
                        help='Only calculate one MD5 for YUV 3 channel combined.')
    parser.add_argument('-p', '--padding', type=int, default=0, nargs=1, dest='padding',
                        metavar='<padding>',
                        help='YUV right padding (in pixels).')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--md5', dest='use_md5', action='store_true',
                        help='Calculate MD5 checksum (default is true).')
    group.add_argument('--crc', dest='use_crc32', action='store_true',
                        help='Calculate CRC32 instead of MD5.')
    group.add_argument('--sha', dest='use_sha1', action='store_true',
                        help='Calculate SHA1 instead of MD5.')

    #parser.print_help()
    args = parser.parse_args(sys.argv[1:])
    if not args.use_crc32 and not args.use_sha1: args.use_md5 = True

    return args

def main():
    args = argParse()
    #print(args)

if __name__ == '__main__':
    main()

