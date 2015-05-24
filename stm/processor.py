#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# stm/processor.py
# 
# Process list of image(s) and or folder(s)
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from image import Image

import os.path as path
from os import listdir

class Processor:
    def __init__(self, conf):
        self.configuration = conf
    
    def process(self):
        self.parseList(self.configuration.input)
        
    def parseList(self, l):
        for name in l:
            
            # parse directories recursively
            if path.isdir(name):
                if self.configuration.recursive:
                    self.parseList([ path.join(name, f) for f in listdir(name)])
                else:
                    self.parseList([ path.join(name, f) for f in listdir(name) if path.isfile(path.join(name, f)) ])
            
            # generate thumbnail if is image
            else:
                img = Image(self.configuration)
                if img.loadImage(name):
                    img.saveThumbnail()