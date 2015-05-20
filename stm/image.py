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

class Image:
    def __init__(self, conf):
        self.image = None
        self.configuration = conf
    
    def loadImage(self, filename):
        pass
    
    def saveThumbnail(self):
        pass

    def getThumbnailName(self):
        pass
    
    def getThumbnailSize(self):
        pass
        
    def getThumbnailBox(self):
        pass
