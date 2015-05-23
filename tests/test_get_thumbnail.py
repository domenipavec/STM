#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# tests/test_filename.py
# 
# Test thumbnail file name generation.
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from unittest import TestCase

from stm.configuration import Configuration
from stm.image import Image

from numpy.linalg import norm

from random import randint
import numpy as np

import cv2

class Test_get_thumbnail(TestCase):
    
    def loadImage(self, name):
        return cv2.imread('examples/' + name + '.png', cv2.IMREAD_UNCHANGED)
    
    def setUp(self):
        self.conf = Configuration()
    
    def tearDown(self):
        self.conf = None

    def test_get_thumbnail(self):
        self.conf.paddColor = (0, 0, 255, 255)
        
        for mode in ['none', 'padd', 'crop']:
            self.conf.cropMode = mode
            
            for name in ['landscape', 'square', 'portrait']:
                loaded_img = self.loadImage(name)
                loaded_thumb = self.loadImage(name + '_thumb_' + mode)
                
                # create thumbnail
                img = Image(self.conf)
                img.image = loaded_img
                thumb = img.getThumbnail()
                
                # difference of matrices normalized
                c = float(sum(sum(sum((loaded_thumb.astype(int) - thumb.astype(int))**2))))**0.5/sum(sum(sum(loaded_thumb.astype(int))))
                print('Mode ' + name + ': ' + str(c))
                
                self.assertFalse(c > 0.0005)
 