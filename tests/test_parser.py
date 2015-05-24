#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# tests/test_parser.py
# 
# Test input arguments parser
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from unittest import TestCase

import argparse, sys

from stm.configuration import Configuration
from stm.parser import Parser


# change argument parser to print to stdout
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stdout)
        print('%s: error: %s\n' % (self.prog, message))
        exit()

class Test_parser(TestCase):

    def setUp(self):
        self.parser = Parser()
    
    def tearDown(self):
        self.parser = None

    def getConf(self, arguments):
        return self.parser.getConfiguration(arguments.split(), ArgumentParser)
    
    def assertInvalid(self, input):
        with self.assertRaises(SystemExit):
            self.getConf(input)
    
    def test_empty(self):
        self.assertInvalid('')
    
    def test_direct(self):
        conf = self.getConf('--input test.png test2.png --prefix pref --postfix post --folder fol')
        self.assertItemsEqual(conf.input, ['test.png', 'test2.png'])
        self.assertEqual(conf.name_prefix, 'pref')
        self.assertEqual(conf.name_postfix, 'post')
        self.assertEqual(conf.folder, 'fol')
    
    def test_output(self):
        self.assertInvalid('--input test.png test2.png --output test.png')
        self.assertInvalid('--input . --output test.png')
        
        conf = self.getConf('--input test.png --output test.png')
        self.assertEqual(conf.output, 'test.png')

    def test_recursive(self):
        conf = self.getConf('--input test.png --recursive')
        self.assertTrue(conf.recursive)
        
        conf = self.getConf('--input test.png')
        self.assertFalse(conf.recursive)
    
    def test_verbose(self):
        conf = self.getConf('--input test.png --verbose')
        self.assertTrue(conf.verbose)
        
        conf = self.getConf('--input test.png')
        self.assertFalse(conf.verbose)
    
    def test_file_format(self):
        conf = self.getConf('--input test.png --fileFormat jpg')
        self.assertEqual(conf.fileFormat, 'jpg')
        
        self.assertInvalid('--input test.png --fileFormat krn')
    
    def test_size(self):
        conf = self.getConf('--input test.png --size 123x456')
        self.assertEqual(conf.size, [123, 456])
        
        self.assertInvalid('--input test.png --size 0x2')
        self.assertInvalid('--input test.png --size -12x2')
        self.assertInvalid('--input test.png --size 123')
        self.assertInvalid('--input test.png --size 12x12x12')
        self.assertInvalid('--input test.png --size xxx')
    
    def test_mode(self):
        conf = self.getConf('--input test.png --scale')
        self.assertEqual(conf.cropMode, 'none')
        
        conf = self.getConf('--input test.png --padd')
        self.assertEqual(conf.cropMode, 'padd')
        
        conf = self.getConf('--input test.png --crop')
        self.assertEqual(conf.cropMode, 'crop')
        
        conf = self.getConf('--input test.png --smart')
        self.assertEqual(conf.cropMode, 'smart')
        
        conf = self.getConf('--input test.png')
        self.assertEqual(conf.cropMode, 'smart')
        
        self.assertInvalid('--input test.png --scale --padd')
        self.assertInvalid('--input test.png --padd --crop')
        self.assertInvalid('--input test.png --crop --featured a')
        self.assertInvalid('--input test.png --featured a --smart')
        self.assertInvalid('--input test.png --smart --scale')
    
    def test_mode_featured(self):
        conf = self.getConf('--input test.png --featured 100x30,-15x30')
        self.assertEqual(conf.featured, ([100,30], [-15, 30]))
        
        self.assertInvalid('--input test.png --featured xxx,xxx')
        self.assertInvalid('--input test.png --featured 10x10x10,15x30')
        self.assertInvalid('--input test.png --featured 10x10,10x10,10x10')
        self.assertInvalid('--input test.png --featured 10x10')
        self.assertInvalid('--input test.png --featured 10,10x10')

    def test_padd_color(self):
        conf = self.getConf('--input test.png --padd --paddColor 0,100,200,250')
        self.assertEqual(conf.paddColor, [0,100,200,250])
        
        conf = self.getConf('--input test.png --padd --paddColor 0,100,200')
        self.assertEqual(conf.paddColor, [0,100,200,255])
        
        self.assertInvalid('--input test.png --padd --paddColor 0')
        self.assertInvalid('--input test.png --padd --paddColor 0,100')
        self.assertInvalid('--input test.png --padd --paddColor 0,100,100,100,100')
        self.assertInvalid('--input test.png --padd --paddColor -1,100,100')
        self.assertInvalid('--input test.png --padd --paddColor 256,100,100')
        self.assertInvalid('--input test.png --paddColor 0,100,100')

    def test_zoominess(self):
        conf = self.getConf('--input test.png --zoominess 10')
        self.assertEqual(conf.zoominess, 10)

        conf = self.getConf('--input test.png --zoominess 0')
        self.assertEqual(conf.zoominess, 0)
        
        self.assertInvalid('--input test.png --zoominess 101')
        self.assertInvalid('--input test.png --zoominess -1')
        self.assertInvalid('--input test.png --zoominess 45 --padd')
        self.assertInvalid('--input test.png --zoominess 45 --crop')
        self.assertInvalid('--input test.png --zoominess 45 --scale')
