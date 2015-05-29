#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# tests/test_get_thumbnail.py
# 
# Test thumbnails against hand created ones.
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from unittest import TestCase

from stm.configuration import Configuration
from stm.image import Image

import cv2

class Test_get_thumbnail(TestCase):
    
    def loadImage(self, name):
        return cv2.imread('examples/' + name + '.png', cv2.IMREAD_UNCHANGED)

    def loadThumb(self, name):
        return cv2.imread('thumbnails/' + name + '.png', cv2.IMREAD_UNCHANGED)
    
    def setUp(self):
        self.conf = Configuration()
    
    def tearDown(self):
        self.conf = None

    def assertImageEqual(self, img1, img2, accuracy):
        # difference of matrices normalized
        c = float(sum(sum(sum((img1.astype(int) - img2.astype(int))**2))))**0.5/sum(sum(sum(img1.astype(int))))
        print(c)
        self.assertFalse(c > accuracy)

    def compareGeneratedLoaded(self, imgname, thumbname, accuracy = 0.0004):
        loaded_img = self.loadImage(imgname)
        loaded_thumb = self.loadThumb(thumbname)
        
        # create thumbnail
        img = Image(self.conf)
        img.image = loaded_img
        thumb = img.getThumbnail()
        
        #cv2.imwrite('/tmp/test/output.png', thumb)
        
        self.assertImageEqual(loaded_thumb, thumb, accuracy)

    def test_get_thumbnail(self):
        self.conf.paddColor = (0, 0, 255, 255)
        
        for mode in ['none', 'padd', 'crop']:
            self.conf.cropMode = mode
            
            for name in ['landscape', 'square', 'portrait']:
                print('Mode: ' + mode + ' Name: ' + name)
                self.compareGeneratedLoaded(name, name + '_thumb_' + mode)

    def test_get_thumbnail_featured(self):
        self.conf.cropMode = 'featured'
        self.conf.featured = [[280,120], [560, 440]]
        
        self.conf.zoominess = 0
        self.compareGeneratedLoaded('featured', 'featured_thumb_0')
        
        self.conf.zoominess = 100
        self.compareGeneratedLoaded('featured', 'featured_thumb_100')
        
        self.conf.zoominess = 50
        self.compareGeneratedLoaded('featured', 'featured_thumb_50', 0.0006)
    
    def test_get_thumbnail_featured_allow_padd(self):
        self.conf.cropMode = 'featured'
        self.conf.allowPadd = True
        self.conf.featured = [[0,0], [-1,-1]]
        self.conf.zoominess = 0
        self.conf.paddColor = (0, 0, 255, 255)
        
        self.compareGeneratedLoaded('landscape', 'landscape_thumb_padd', 0.0006)
        self.compareGeneratedLoaded('portrait', 'portrait_thumb_padd', 0.0007)
        self.compareGeneratedLoaded('square', 'square_thumb_padd')
