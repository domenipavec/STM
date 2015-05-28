#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# stm/image.py
# 
# Image representation, contains functions for image manipulation.
# ----------------------------------------------------------------
# copyright (c) 2015 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

import os.path, cv2, os
import numpy as np

class Image:
    def __init__(self, conf):
        self.image = None
        self.configuration = conf
    
    def loadImage(self, fn):
        self.filename = fn
        self.image = cv2.imread(self.filename, cv2.IMREAD_UNCHANGED)
        if self.image == None:
            return False
        else:
            return True
    
    def saveThumbnail(self):
        thumb = self.getThumbnail()
        name = self.getThumbnailName()
        if self.configuration.verbose:
            print(name)
        cv2.imwrite(name, thumb)

    # Construct name for thumbnail based on image name and configuration
    def getThumbnailName(self):
        if self.configuration.output != None:
            return self.configuration.output
        
        path, name = os.path.split(self.filename)
        name, ext = os.path.splitext(name)
        
        if self.configuration.fileFormat != 'source':
            ext = '.' + self.configuration.fileFormat
        
        folder = ''
        if self.configuration.folder == None \
            and self.configuration.name_prefix == '' \
            and self.configuration.name_postfix == '':
            folder = 'thumbs'
        elif self.configuration.folder != None:
            folder = self.configuration.folder
        
        path = os.path.join(path, folder)
        if path and not os.path.exists(path):
            os.mkdir(path)
        
        name = self.configuration.name_prefix + name + \
            self.configuration.name_postfix + ext
        
        return os.path.join(path, name)
    
    # transform image to thumbnail size in cropMode
    def getThumbnail(self):
        thumbFunc = getattr(self, 'getThumbnail_' + self.configuration.cropMode)
        return thumbFunc()
    
    # thumbnail with scale only
    def getThumbnail_none(self):
        scale = min(float(self.configuration.size[0])/self.image.shape[1],
                    float(self.configuration.size[1])/self.image.shape[0])
        return cv2.resize(self.image, None, fx=scale, fy=scale, interpolation=self.configuration.resizeInterpolation)
    
    # thumbnail with padding
    def getThumbnail_padd(self):
        scale = min(float(self.configuration.size[0])/self.image.shape[1],
                    float(self.configuration.size[1])/self.image.shape[0])
        thumb = cv2.resize(self.image, None, fx=scale, fy=scale, interpolation=self.configuration.resizeInterpolation)
        
        # calculate required padding
        horizontal = int(self.configuration.size[0] - thumb.shape[1])
        left = horizontal/2
        right = horizontal - left
        vertical = int(self.configuration.size[1] - thumb.shape[0])
        top = vertical/2
        bottom = vertical - top
        return cv2.copyMakeBorder(thumb, top, bottom, left, right, \
                                  cv2.BORDER_CONSTANT, value=self.configuration.paddColor)
    
    # thumbnail with crop
    def getThumbnail_crop(self):
        scale = max(float(self.configuration.size[0])/self.image.shape[1],
                    float(self.configuration.size[1])/self.image.shape[0])
        
        # calculate required crop
        horizontal = int(self.image.shape[1] - round(self.configuration.size[0]/scale))
        left = horizontal/2
        right = horizontal - left
        vertical = int(self.image.shape[0] - round(self.configuration.size[1]/scale))
        top = vertical/2
        bottom = vertical - top
        cropped = self.image[top:self.image.shape[0]-bottom, left:self.image.shape[1]-right]
        return cv2.resize(cropped, None, fx=scale, fy=scale, interpolation=self.configuration.resizeInterpolation)
    
    def getThumbnail_featured(self):
        area_center = [0,0]
        area_dimension = [0,0]
        
        # calculate coordinates for interesting area
        for point in self.configuration.featured:
            # negative coordinates start at right and bottom
            x = point[0]
            y = point[1]
            if x < 0:
                x += self.image.shape[1]
            if y < 0:
                y += self.image.shape[0]
            
            if x < 0 or x >= self.image.shape[1] or \
                y < 0 or y >= self.image.shape[0]:
                raise Exception("Featured point " + str((x,y)) + " out of image " + str([self.image.shape[1], self.image.shape[0]]) + "!")
            
            area_center[0] += x
            area_center[1] += y
            
            if area_dimension[0] == 0:
                area_dimension[0] = x
            else:
                area_dimension[0] -= x
            if area_dimension[1] == 0:
                area_dimension[1] = y
            else:
                area_dimension[1] -= y
        
        area_center[0] /= 2
        area_center[1] /= 2
        
        area_dimension[0] = abs(area_dimension[0])
        area_dimension[1] = abs(area_dimension[1])
        
        # scale when max zoomed in
        max_scale = min(float(self.configuration.size[0])/area_dimension[0],
                    float(self.configuration.size[1])/area_dimension[1])
        
        # scale when whole image in thumb
        min_scale = max(float(self.configuration.size[0])/self.image.shape[1],
                    float(self.configuration.size[1])/self.image.shape[0])
        
        # if max zoom more out than whole thumb, correct
        if min_scale > max_scale:
            min_scale = max_scale
        
        # scale is inverse in size, so linear fit between sizes based on zoominess
        scale = 1/((1/max_scale-1/min_scale)/100*self.configuration.zoominess + 1/min_scale)
        
        # calculate actual base image area size based on actual scale
        actual_area_size = [round(self.configuration.size[0]/scale), round(self.configuration.size[1]/scale)]
        
        # calculate base image area 
        left = max(area_center[0] - actual_area_size[0]/2, 0)
        right = left + actual_area_size[0]
        top = max(area_center[1] - actual_area_size[1]/2, 0)
        bottom = top + actual_area_size[1]
        
        cropped = self.image[top:bottom, left:right]
        return cv2.resize(cropped, None, fx=scale, fy=scale, interpolation=self.configuration.resizeInterpolation)
    
    def getThumbnail_smart(self):
        return np.zeros((self.configuration.size[1], self.configuration.size[0], 4))
