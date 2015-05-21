#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# stm/image.py
# 
# Image representation, contains functions for image manipulation.
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

import os.path

class Image:
    def __init__(self, conf):
        self.image = None
        self.configuration = conf
    
    def loadImage(self, fn):
        self.filename = fn
    
    def saveThumbnail(self):
        pass

    # Construct name for thumbnail based on image name and configuration
    def getThumbnailName(self):
        if self.configuration.output != None:
            return self.configuration.output
        
        path, name = os.path.split(self.filename)
        name, ext = os.path.splitext(name)
        
        if self.configuration.fileFormat != 'source':
            ext = '.' + self.configuration.fileFormat
        
        folder = ''
        if self.configuration.folder == None \
            and self.configuration.name_prefix == '' \
            and self.configuration.name_postfix == '':
            folder = 'thumbs'
        elif self.configuration.folder != None:
            folder = self.configuration.folder
            
        name = self.configuration.name_prefix + name + \
            self.configuration.name_postfix + ext
        
        return os.path.join(path, folder, name)
    
    def getThumbnailSize(self):
        pass
        
    def getThumbnailBox(self):
        pass
