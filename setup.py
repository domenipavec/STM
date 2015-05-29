#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# setup.py
# 
# setup for STM
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from setuptools import setup, find_packages

try:
    import cv2
except ImportError:
    print("OpenCV for Python is required and is not installed.\nPlease install OpenCV and try again.")
    exit()

setup(
    name='STM',
    
    version='0.1',
    
    packages=['stm'],
    
    test_suite='nose.collector',
    
    install_requires=['nose'],
    
    entry_points={
        'console_scripts': [
            'stm=stm:main',
        ],
    },
    
    package_data={
        'stm': [ 'data/haarcascade_frontalface_default.xml' ],
    }
)
