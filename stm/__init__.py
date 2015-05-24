#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# stm/__init__.py
# 
# main entry point
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from stm.parser import Parser
from stm.processor import Processor

def main():
    """Entry point for the application script"""
    
    parser = Parser()
    
    # parse command line arguments
    conf = parser.getConfiguration()
    
    processor = Processor(conf)
    
    # generate thumbnails
    processor.process()