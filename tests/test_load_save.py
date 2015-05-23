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

from numpy.testing import assert_array_equal
from tempfile import tempdir
import os.path as path
import os

import cv2
import numpy as np

class Test_load_save(TestCase):
    
    def loadImage(self, name):
        return cv2.imread('examples/' + name + '.png', cv2.IMREAD_UNCHANGED)
    
    def setUp(self):
        self.tempfile = path.join(tempdir, 'test.png')
        self.conf = Configuration()
        self.conf.output = self.tempfile
        self.conf.cropMode = 'none'
    
    def tearDown(self):
        self.conf = None

    def test_load_image(self):
        img = Image(self.conf)
        img.loadImage('examples/landscape.png')
        loaded_img = self.loadImage('landscape')
        assert_array_equal(loaded_img, img.image)
 
    def test_save_thumbnail(self):
        generated_img = np.zeros((100,100,4))
        img = Image(self.conf)
        img.image = generated_img
        img.saveThumbnail()
        
        assert(path.isfile(self.tempfile))
        
        loaded_img = cv2.imread(self.tempfile, cv2.IMREAD_UNCHANGED)
        assert_array_equal(loaded_img, generated_img)
        
        os.remove(self.tempfile)