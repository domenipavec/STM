#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# tests/test_image_size.py
# 
# Test thumbnail size.
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from unittest import TestCase

from stm.configuration import Configuration
from stm.image import Image

import numpy as np
import cv2

class Test_image_size(TestCase):
    def getPortraitThumb(self):
        img = Image(self.conf)
        img.image = np.zeros((300, 200, 4), np.uint8)
        return img.getThumbnail()

    def getLandscapeThumb(self):
        img = Image(self.conf)
        img.image = np.zeros((200, 300, 4), np.uint8)
        return img.getThumbnail()
    
    def getSquareThumb(self):
        img = Image(self.conf)
        img.image = np.zeros((200, 200, 4), np.uint8)
        return img.getThumbnail()
    
    def checkSize(self, img, size):
        self.assertEqual(img.shape[1], size[0])
        self.assertEqual(img.shape[0], size[1])
    
    def setUp(self):
        self.conf = Configuration()
    
    def tearDown(self):
        self.conf = None
    
    def test_mode_none(self):
        self.conf.cropMode = "none"
        
        img_p = self.getPortraitThumb()
        img_l = self.getLandscapeThumb()
        img_s = self.getSquareThumb()
        
        self.checkSize(img_p, (67, 100))
        self.checkSize(img_l, (100, 67))
        self.checkSize(img_s, (100,100))
    
    def test_mode_other(self):
        self.conf.featured = [[0,0],[100,100]]
        for mode in ['padd', 'crop', 'featured', 'smart']:
            self.conf.cropMode = mode
            
            img_p = self.getPortraitThumb()
            img_l = self.getLandscapeThumb()
            img_s = self.getSquareThumb()
            
            self.checkSize(img_p, (100, 100))
            self.checkSize(img_l, (100, 100))
            self.checkSize(img_s, (100,100))        
 