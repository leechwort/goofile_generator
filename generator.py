#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:42:02 2023

@author: artsin
"""
import os
import zipfile
import cv2


def generate_chitubox_zip(image): 
    zf = zipfile.ZipFile("result.zip", "w")
    zf.write("./data/run.gcode", "./run.gcode")
    zf.write("./data/preview.png", "./preview.png")
    zf.write("./data/preview_cropping.png", "./preview_cropping.png")
    zf.write("./1.png", "./1.png")
#for dirname, subdirs, files in os.walk("./"):
#    zf.write(dirname)
#    for filename in files:
#        zf.write(os.path.join(dirname, filename))
    zf.close()


from PIL import Image


def combine_images(columns, space, images):
    rows = len(images) // columns
    if len(images) % columns:
        rows += 1
    #width_max = max([Image.open(image).width for image in images])
    width_max = 11520
    height_max = 5120
    #height_max = max([Image.open(image).height for image in images])
    background_width = width_max*columns + (space*columns)-space
    background_height = height_max*rows + (space*rows)-space
    background = Image.new('RGBA', (width_max, height_max), (0, 0, 0, 255))
    x = 0
    y = 0
    for i, image in enumerate(images):
        img = Image.open(image)
        x_offset = 200*i
        y_offset = 200*i
        background.paste(img, (x_offset, y_offset))
        #x += width_max + space
        #if (i+1) % columns == 0:
        #    y += height_max + space
        #    x = 0
    background.save('1.png')

def generate_bulk_markers():
    #marker_size = 6
    marker_size = 100
    num_markers = 9
    marker_imgs = []
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    
    for marker_id in range(num_markers):
        marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
        fname = "./markers/marker_{}.png".format(marker_id)
        cv2.imwrite(fname, marker_img)
        #marker_imgs.append(cv2.imread("./markers/marker_{}.png".format(marker_id)))
        marker_imgs.append(fname)
    return marker_imgs

x = generate_bulk_markers()
print(x)
combine_images(columns=3, space=20, images=x)
generate_chitubox_zip(None)