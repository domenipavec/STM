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
        
        # convert image to BGRA
        if len(self.image.shape) == 2:
            old_image = self.image
            self.image = np.empty((self.image.shape[0], self.image.shape[1], 4), dtype=np.uint8)
            self.image[:, :, 0] = old_image[:, :]
            self.image[:, :, 1] = old_image[:, :]
            self.image[:, :, 2] = old_image[:, :]
            self.image[:, :, 3] = 255
        
        elif self.image.shape[2] == 1:
            old_image = self.image
            self.image = np.empty((self.image.shape[0], self.image.shape[1], 4), dtype=np.uint8)
            self.image[:, :, 0] = old_image[:, :, 0]
            self.image[:, :, 1] = old_image[:, :, 0]
            self.image[:, :, 2] = old_image[:, :, 0]
            self.image[:, :, 3] = 255
            
        elif self.image.shape[2] == 3:
            old_image = self.image
            self.image = np.empty((self.image.shape[0], self.image.shape[1], 4), dtype=np.uint8)
            self.image[:, :, 0:3] = old_image[:, :, 0:3]
            self.image[:, :, 3] = 255

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
    
    # Resize function that uses correct interpolation based on scale
    def resize(self, scale_x, scale_y = None, img=None):
        if scale_y == None:
            scale_y = scale_x

        if scale_x > 1.0 or scale_y > 1.0:
            interpol = cv2.INTER_CUBIC
        else:
            interpol = cv2.INTER_AREA
        
        if img == None:
            img = self.image
        
        return cv2.resize(img, None, fx=scale_x, fy=scale_y, interpolation=interpol)
        
    
    # transform image to thumbnail size in cropMode
    def getThumbnail(self):
        thumbFunc = getattr(self, 'getThumbnail_' + self.configuration.cropMode)
        return thumbFunc()
    
    # thumbnail with scale only
    def getThumbnail_none(self):
        scale = min(float(self.configuration.size[0])/self.image.shape[1],
                    float(self.configuration.size[1])/self.image.shape[0])
        return self.resize(scale)
    
    # thumbnail with padding
    def getThumbnail_padd(self):
        scale = min(float(self.configuration.size[0])/self.image.shape[1],
                    float(self.configuration.size[1])/self.image.shape[0])
        thumb = self.resize(scale)
        
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
        return self.resize(scale, img=cropped)
    
    # thumbnail with featured area
    def getThumbnail_featured(self, lefttop = None, rightbottom = None):
        area_center = [0,0]
        area_dimension = [0,0]
        
        if lefttop == None:
            points = self.configuration.featured
        else:
            points = [lefttop, rightbottom]
        
        # calculate coordinates for interesting area
        for point in points:
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
        
        area_dimension[0] = abs(area_dimension[0]) + 1
        area_dimension[1] = abs(area_dimension[1]) + 1
        if self.configuration.testing:
            print("Area dimension: " + str(area_dimension))
            print("Area center: " + str(area_center))
        
        # scale when max zoomed in
        max_scale = min(float(self.configuration.size[0])/area_dimension[0],
                    float(self.configuration.size[1])/area_dimension[1])
        
        # scale when whole image in thumb
        min_scale = max(float(self.configuration.size[0])/self.image.shape[1],
                    float(self.configuration.size[1])/self.image.shape[0])

        if self.configuration.testing:
            print("Scales: " + str((min_scale, max_scale)))
        
        # if area bigger than whole image in thumb correct
        if min_scale > max_scale:
            # add padding if allowed
            if self.configuration.allowPadd:
                min_scale = max_scale
                # add padding
                horizontal = max(int(round(self.configuration.size[0]/min_scale)) - self.image.shape[1], 0)
                left = horizontal/2
                right = horizontal - left
                vertical = max(int(round(self.configuration.size[1]/min_scale)) - self.image.shape[0], 0)
                top = vertical/2
                bottom = vertical - top
                self.image = cv2.copyMakeBorder(self.image, top, bottom, left, right, \
                                        cv2.BORDER_CONSTANT, value=self.configuration.paddColor)
            else:
                max_scale = min_scale
        
        # scale is inverse in size, so linear fit between sizes based on zoominess
        scale = 1/((1/max_scale-1/min_scale)/100*self.configuration.zoominess + 1/min_scale)
        if self.configuration.testing:
            print("Scale: " + str(scale))
        
        # calculate actual base image area size based on actual scale
        actual_area_size = [round(self.configuration.size[0]/scale), round(self.configuration.size[1]/scale)]
        if self.configuration.testing:
            print("Actual area size: " + str(actual_area_size))
            print("Actual image size: " + str((self.image.shape[1], self.image.shape[0])))
        
        # calculate base image area 
        left = max(area_center[0] - actual_area_size[0]/2, 0)
        right = min(left + actual_area_size[0], self.image.shape[1])
        left = max(right - actual_area_size[0], 0)
        
        top = max(area_center[1] - actual_area_size[1]/2, 0)
        bottom = min(top + actual_area_size[1], self.image.shape[0])
        top = max(bottom - actual_area_size[1], 0)
        
        if self.configuration.testing:
            print("Base image area: " + str((left,right,top,bottom)))
        
        cropped = self.image[top:bottom, left:right]
        if self.configuration.testing:
            print("Cropped size: " + str((cropped.shape[1], cropped.shape[0])))
        
        # correct scale, otherwise final image can be wrong dimesions by a few pixels
        corrected_scale_x = float(self.configuration.size[0])/actual_area_size[0]
        corrected_scale_y = float(self.configuration.size[1])/actual_area_size[1]
        if self.configuration.testing:
            assert(abs(corrected_scale_x - scale)/scale < 0.01)
            assert(abs(corrected_scale_y - scale)/scale < 0.01)
            print("Corrected scale: " + str((corrected_scale_x, corrected_scale_y)))
        
        resized = self.resize(corrected_scale_x, corrected_scale_y, cropped)
        if self.configuration.testing:
            print("Resized size: " + str((resized.shape[1], resized.shape[0])))
            
        return resized
    
    # detect featured area automatically, then use getThumbnail_featured
    def getThumbnail_smart(self):
        # load face detection
        if self.configuration.faceCascade == None:
            self.configuration.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # do detection on small image
        scale = max(200.0/self.image.shape[1],
                        200.0/self.image.shape[0])
        resized = cv2.resize(self.image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        # face detection
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        faces = self.configuration.faceCascade.detectMultiScale(
            gray,
        )

        # edge detection
        blur = cv2.GaussianBlur(resized,(5,5),0)
        edges = cv2.Canny(blur,100,200)

        # get edge coordinates
        nz = np.nonzero(edges)

        # calculate average and min and max
        average = [0, 0]
        divider = [0, 0]
        minimum = [resized.shape[1] - 1, resized.shape[0] - 1]
        maximum = [0, 0]
        for d in range(2):
            for i in range(len(nz[d])):
                average[d] += nz[1-d][i]
                divider[d] += 1
                if nz[1-d][i] < minimum[d]:
                    minimum[d] = nz[1-d][i]
                if nz[1-d][i] > maximum[d]:
                    maximum[d] = nz[1-d][i]
            if divider[d] != 0:
                average[d] = float(average[d])/divider[d]

        # calculate standard diviation
        sd = [0, 0]
        divider = [0, 0]
        for d in range(2):
            for i in range(len(nz[d])):
                sd[d] += (average[d] - nz[1-d][i])**2
                divider[d] += 1
            if divider[d] != 0:
                sd[d] = (float(sd[d])/divider[d])**0.5

        # calculate bounding box based on average and sd
        lefttop = [0,0]
        rightbottom = [0,0]
        for d in range(2):
            lefttop[d] = max(int(round(average[d] - 1.5*sd[d])), 0)
            rightbottom[d] = min(int(round(average[d] + 1.5*sd[d])), edges.shape[1-d] - 1)

        # draw average and sd box and center
        if self.configuration.debug:
            cv2.rectangle(resized, tuple(lefttop), tuple(rightbottom), (0,0,255), 3)
            cv2.circle(resized, (int(average[0]), int(average[1])), 10, (0,255,0), -1)

        # if min*max area is small, replace bounding box with it
        if (maximum[0]-minimum[0])*(maximum[1]-minimum[1]) < 0.8*resized.shape[0]*resized.shape[1]:
            lefttop = minimum
            rightbottom = maximum
        
        # draw min max area
        if self.configuration.debug:
            cv2.rectangle(resized, tuple(minimum), tuple(maximum), (255, 255, 0), 3)

        # extend area with faces
        for (x,y,w,h) in faces:
            face_lefttop = (x,y)
            face_rightbottom = (x+w, y+h)
            for d in range(2):
                if face_lefttop[d] < lefttop[d]:
                    lefttop[d] = face_lefttop[d]
                if face_rightbottom[d] > rightbottom[d]:
                    rightbottom[d] = face_rightbottom[d]
            
            # draw face
            if self.configuration.debug:
                cv2.rectangle(resized, tuple(face_lefttop), tuple(face_rightbottom), (255,0,0), 2)

        # draw final area
        if self.configuration.debug:
            cv2.rectangle(resized, tuple(lefttop), tuple(rightbottom), (0, 255, 255), 2)
        
        # write debug image
        if self.configuration.debug:
            path, name = os.path.split(self.filename)
            path = os.path.join(path, 'debug')
            if not os.path.exists(path):
                os.mkdir(path)
            filename = os.path.join(path, name)
            cv2.imwrite(filename, resized)
        
        # scale points back to full size
        for d in range(2):
            lefttop[d] = int(round(lefttop[d]/scale))
            rightbottom[d] = int(round(rightbottom[d]/scale))
        
        return self.getThumbnail_featured(lefttop, rightbottom)
