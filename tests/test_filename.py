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

import os, os.path

class Test_filename(TestCase):
    def checkImage(self, input, output):
        img = Image(self.conf)
        img.loadImage(input)
        self.assertEqual(img.getThumbnailName(), output)
    
    def setUp(self):
        self.conf = Configuration()
    
    def removeFolders(self, l):
        for f in l:
            if os.path.exists(f):
                try:
                    os.rmdir(f)
                except:
                    pass
    
    def tearDown(self):
        self.conf = None
        self.removeFolders(('thumbs', '/tmp/thumbs', 'test', '/tmp/test', 'test-folder', '/tmp/test-folder'))
    
    def test_output_file(self):
        self.conf.output = "output.jpg"
        self.checkImage("input.png", "output.jpg")
    
    def test_no_config(self):
        self.checkImage("input.png", "thumbs/input.png")
        self.checkImage("input.jpg", "thumbs/input.png")
        self.checkImage("13 De_(com)čšž.test.jpg", "thumbs/13 De_(com)čšž.test.png")
        self.checkImage("/tmp/input.jpg", "/tmp/thumbs/input.png")

    def test_folder(self):
        self.conf.folder = "test-folder"
        self.checkImage("input.png", "test-folder/input.png")
        self.checkImage("input.jpg", "test-folder/input.png")
        self.checkImage("13 De_(com)čšž.test.jpg", "test-folder/13 De_(com)čšž.test.png")
        self.checkImage("/tmp/input.jpg", "/tmp/test-folder/input.png")

    def test_abs_folder(self):
        self.conf.folder = "/tmp"
        self.checkImage("input.png", "/tmp/input.png")
        self.checkImage("input.jpg", "/tmp/input.png")
        self.checkImage("13 De_(com)čšž.test.jpg", "/tmp/13 De_(com)čšž.test.png")
        self.checkImage("/tmp/input.jpg", "/tmp/input.png")

    def test_format_jpg(self):
        self.conf.fileFormat = 'jpg'
        self.checkImage("input.png", "thumbs/input.jpg")
        self.checkImage("input.jpg", "thumbs/input.jpg")
        self.checkImage("13 De_(com)čšž.test.jpg", "thumbs/13 De_(com)čšž.test.jpg")
        self.checkImage("/tmp/input.jpg", "/tmp/thumbs/input.jpg")
        
    def test_format_source(self):
        self.conf.fileFormat = 'source'
        self.checkImage("input.png", "thumbs/input.png")
        self.checkImage("image.jpg", "thumbs/image.jpg")
        self.checkImage("13 De_(com)čšž.test.jpg", "thumbs/13 De_(com)čšž.test.jpg")
        self.checkImage("/tmp/input.png", "/tmp/thumbs/input.png")

    def test_postfix(self):
        self.conf.name_postfix = "_thumb"
        self.checkImage("input.png", "input_thumb.png")
        self.checkImage("input.jpg", "input_thumb.png")
        self.checkImage("13 De_(com)čšž.test.jpg", "13 De_(com)čšž.test_thumb.png")
        self.checkImage("/tmp/input.jpg", "/tmp/input_thumb.png")

    def test_prefix(self):
        self.conf.name_prefix = "thumb_"
        self.checkImage("input.png", "thumb_input.png")
        self.checkImage("input.jpg", "thumb_input.png")
        self.checkImage("13 De_(com)čšž.test.jpg", "thumb_13 De_(com)čšž.test.png")
        self.checkImage("/tmp/input.jpg", "/tmp/thumb_input.png")
    
    def test_all(self):
        self.conf.folder = "test"
        self.conf.fileFormat = 'jpg'
        self.conf.name_prefix = "thumb_"
        self.conf.name_postfix = "_thumb"
        self.checkImage("input.png", "test/thumb_input_thumb.jpg")
        self.checkImage("input.jpg", "test/thumb_input_thumb.jpg")
        self.checkImage("13 De_(com)čšž.test.jpg", "test/thumb_13 De_(com)čšž.test_thumb.jpg")
        self.checkImage("/tmp/input.png", "/tmp/test/thumb_input_thumb.jpg")
