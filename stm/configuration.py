#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# stm/configuration.py
# 
# Holds configuration values.
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

import cv2

class Configuration:
    def __init__(self):
        # file name prefix for folder or multi-image thumbnails
        self.name_prefix = ""
        
        # file name postfix for folder or multi-image thumbnails
        self.name_postfix = ""
        
        # file folder for folder or multi-image thumbnails
        self.folder = "./thumbs/"
        
        # file format for folder or multi-image thumbnails
        self.fileFormat = "png"
        
        # how much zooming is preffered
        self.zoominess = 30
        
        # target image size
        self.size = (100,100)
        
        # input file(s)
        self.input = ""
        
        # output file if specified
        self.output = ""
        
        # featured area if specified
        self.featured = None
        
        # whether image should be cropped to target size
        self.crop = True
        
        # whether featured area should be auto-detected if not specified
        self.smart = True

        # mode for video thumbnails (time or "random" or "random-still")
        self.videoMode = "random-still"
        
        # interpolation to use in resize
        self.resizeInterpolation = cv2.INTER_AREA
