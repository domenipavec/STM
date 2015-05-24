#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# tests/test_processor.py
# 
# Test processor file and folder processing.
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from unittest import TestCase

from stm.configuration import Configuration
from stm.processor import Processor

from tempfile import tempdir
import os.path as path
import os, shutil

class Test_processor(TestCase):

    def assertFiles(self, files):
        if os.path.exists(self.tmpfolder):
            self.assertItemsEqual(os.listdir(self.tmpfolder), files)
        else:
            self.assertItemsEqual([], files)

    def setUp(self):
        self.tmpfolder = path.join(tempdir, 'stm-test/')
        
        self.conf = Configuration()
        self.conf.folder = self.tmpfolder
        self.conf.cropMode = 'none'
    
    def tearDown(self):
        if os.path.exists(self.tmpfolder):
            shutil.rmtree(self.tmpfolder)
        
        self.conf = None

    def test_single_image(self):
        self.conf.input = ('examples/portrait.png',)
        proc = Processor(self.conf)
        proc.process()
        self.assertFiles(('portrait.png',))
    
    def test_two_images(self):
        self.conf.input = ('examples/portrait.png', 'examples/landscape.png')
        proc = Processor(self.conf)
        proc.process()
        self.assertFiles(('portrait.png', 'landscape.png'))
    
    def test_folder(self):
        self.conf.input = ('examples/',)
        proc = Processor(self.conf)
        proc.process()
        self.assertFiles(('portrait.png', 'landscape.png', 'square.png'))
    
    def test_empty_folder(self):
        self.conf.input = ('.',)
        proc = Processor(self.conf)
        proc.process()
        self.assertFiles([])
    
    def test_recursive(self):
        self.conf.input = ('examples/',)
        self.conf.recursive = True
        proc = Processor(self.conf)
        proc.process()
        self.assertFiles(('portrait.png', 'landscape.png', 'square.png', 'recursive-square.png'))
