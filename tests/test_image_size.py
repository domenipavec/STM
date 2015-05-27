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
        
        # test with square thumb
        print("Test: Square thumb")
        self.conf.size = (100,100)
        
        img_p = self.getPortraitThumb()
        img_l = self.getLandscapeThumb()
        img_s = self.getSquareThumb()
        
        self.checkSize(img_p, (67, 100))
        self.checkSize(img_l, (100, 67))
        self.checkSize(img_s, (100,100))
    
        # test with portrait thumb
        print("Test: Portrait thumb")
        self.conf.size = (50, 100)

        img_p = self.getPortraitThumb()
        img_l = self.getLandscapeThumb()
        img_s = self.getSquareThumb()

        self.checkSize(img_p, (50, 75))
        self.checkSize(img_l, (50, 33))
        self.checkSize(img_s, (50, 50))

        # test with landscape thumb
        print("Test: Landscape thumb")
        self.conf.size = (100, 50)

        img_p = self.getPortraitThumb()
        img_l = self.getLandscapeThumb()
        img_s = self.getSquareThumb()

        self.checkSize(img_p, (33, 50))
        self.checkSize(img_l, (75, 50))
        self.checkSize(img_s, (50, 50))

        # test with bigger square image
        print("Test: Square image")
        self.conf.size = (500,500)
        
        img_p = self.getPortraitThumb()
        img_l = self.getLandscapeThumb()
        img_s = self.getSquareThumb()
        
        self.checkSize(img_p, (333, 500))
        self.checkSize(img_l, (500, 333))
        self.checkSize(img_s, (500,500))
    
        # test with bigger portrait image
        print("Test: Portrait image")
        self.conf.size = (500, 1000)

        img_p = self.getPortraitThumb()
        img_l = self.getLandscapeThumb()
        img_s = self.getSquareThumb()

        self.checkSize(img_p, (500, 750))
        self.checkSize(img_l, (500, 333))
        self.checkSize(img_s, (500, 500))

        # test with bigger landscape image
        print("Test: Landscape image")
        self.conf.size = (1000, 500)

        img_p = self.getPortraitThumb()
        img_l = self.getLandscapeThumb()
        img_s = self.getSquareThumb()

        self.checkSize(img_p, (333, 500))
        self.checkSize(img_l, (750, 500))
        self.checkSize(img_s, (500, 500))

        
    def test_mode_other(self):
        self.conf.featured = [[0,0],[100,100]]
        for mode in ['padd', 'crop', 'featured', 'smart']:
            self.conf.cropMode = mode
            for size in [(100,100), (100, 50), (50, 100), (500, 500), (1000, 500), (500, 1000)]:
                self.conf.size = size
                
                print('Test: Mode: ' + mode + ' Size: ' + str(size))
                
                img_p = self.getPortraitThumb()
                img_l = self.getLandscapeThumb()
                img_s = self.getSquareThumb()
                
                self.checkSize(img_p, size)
                self.checkSize(img_l, size)
                self.checkSize(img_s, size)
 
