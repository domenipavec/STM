#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# stm/parser.py
# 
# Parser parses input arguments and constructs Configuration.
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

import argparse
import os.path as path

from stm.configuration import Configuration

class Parser:
    def __init__(self):
        # supported formats from opencv docs
        self.supportedFormats = ('bmp', 'dib', 'jpeg', 'jpg', 'jpe', 'jp2', \
            'png', 'pbm', 'pgm', 'ppm', 'sr', 'ras', 'tiff', 'tif')

    def getConfiguration(self, arguments = None, ArgumentParser = argparse.ArgumentParser):
        parser = ArgumentParser(description="""Resize images.""")
        
        # arguments for file names
        parser.add_argument('--input', '-i', nargs='+', help='Input file(s) and/or folder(s).', required=True)
        parser.add_argument('--output', '-o', help='Output file (only for one input).')
        parser.add_argument('--prefix', help='Thumbnail file name prefix.')
        parser.add_argument('--postfix', help='Thumbnail file name postfix')
        parser.add_argument('--folder', '-f', help='Thumbnail folder (default is "thumb"), can be relative or absolute.')
        parser.add_argument('--recursive', '-r', help='Parse folders recursively.', action='store_true')
        
        parser.add_argument('--verbose', '-v',  help='Print output file(s) name(s).', action='store_true')
        parser.add_argument('--debug', '-d', help='Output debug image for smart algorithm.', action='store_true')
        
        # output file options
        parser.add_argument('--fileFormat', help='Thumbnail format (default is "png"), set to "source" to keep source image format')
        parser.add_argument('--size', '-s', help='Thumbnail size (default is 100x100)')
        
        # crop mode options
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--scale', help='Make thumbnail with regular scale.', action='store_true')
        group.add_argument('--padd', help='Make thumbnail and padd to dimension.', action='store_true')
        group.add_argument('--crop', help='Make thumbnail with cropping.', action='store_true')
        group.add_argument('--featured', help='Specify interesting part of image with two points (e.g. "100x100,150x150"), you can use negative to start at bottom or right.')
        group.add_argument('--smart', help='Automatically detect interesting part of image (default).', action='store_true')
        
        parser.add_argument('--paddColor', help='Color for padding (default is "255,255,255,0"), format is BGRA.')
        parser.add_argument('--zoominess', help='How much to zoom in interesting part (between 0 and 100, default is 30).', type=int)
        parser.add_argument('--allowPadd', help='Allow adding padding when featured area is bigger than max thumb area.', action='store_true')

        args = parser.parse_args(arguments)
        
        conf = Configuration()
        conf.input = args.input
        
        if args.output:
            if len(args.input) > 1 or path.isdir(args.input[0]):
                parser.error("--output Option is only valid for one input file.")
            else:
                conf.output = args.output
                
        if args.prefix:
            conf.name_prefix = args.prefix
            
        if args.postfix:
            conf.name_postfix = args.postfix
            
        conf.folder = args.folder
        conf.recursive = args.recursive
        conf.verbose = args.verbose
        conf.debug = args.debug
        
        if args.fileFormat:
            if args.fileFormat.lower() in self.supportedFormats:
                conf.fileFormat = args.fileFormat
            else:
                parser.error("--fileFormat Unsupported format.")
        
        # should be two positive integers (e.g. 10x10)
        if args.size:
            try:
                parts = [int(x) for x in args.size.split('x') if int(x) > 0]
            except:
                parts = []
            if len(parts) == 2:
                conf.size = parts
            else:
                parser.error("--size Invalid size.")
        
        if args.scale:
            conf.cropMode = 'none'
        elif args.padd:
            conf.cropMode = 'padd'
        elif args.crop:
            conf.cropMode = 'crop'
        elif args.featured:
            conf.cropMode = 'featured'
            # should be two points separated with comma (e.g. 10x10,15x15)
            parts = args.featured.split(',')
            if len(parts) != 2:
                parser.error("--featured Invalid format.")
            try:
                point1 = [int(x) for x in parts[0].split('x')]
            except:
                point1 = []
            try:
                point2 = [int(x) for x in parts[1].split('x')]
            except:
                point2 = []
            if len(point1) != 2:
                parser.error("--featured Point 1 invalid.")
            if len(point2) != 2:
                parser.error("--featured Point 2 invalid.")
            conf.featured = (point1, point2)
        
        if args.paddColor:
            # color is 3 or 4 (with alpha) comma separated values
            parts = [int(x) for x in args.paddColor.split(',') if x.isdigit() and 0 <= int(x) <= 255]
            if len(parts) == 3:
                parts.append(255)
            if len(parts) != 4:
                parser.error("--paddColor Invalid color.")
            conf.paddColor = parts
        
        if type(args.zoominess) is int:
            if conf.cropMode != 'featured' and conf.cropMode != 'smart':
                parser.error("--zoominess Option is only valid in --featured and --smart modes.")
            if 0 <= args.zoominess <= 100:
                conf.zoominess = args.zoominess
            else:
                parser.error("--zoominess Out of range")
        
        conf.allowPadd = args.allowPadd
        
        return conf