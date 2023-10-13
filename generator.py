#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:42:02 2023
@author: artsin
"""
import os
import zipfile
import cv2

PIXEL_RATIO = 24/19
REAL_DISPLAY_WIDTH = 11520
REAL_DISPLAY_HEIGHT = 5120
VIRT_DISPLAY_WIDTH = 11520
VIRT_DISPLAY_HEIGHT = int(REAL_DISPLAY_HEIGHT * PIXEL_RATIO)


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


from PIL import Image, ImageEnhance, ImageFont, ImageDraw

def generate_calibration_grid():
    width_max = VIRT_DISPLAY_WIDTH
    height_max = VIRT_DISPLAY_HEIGHT
    step = 60
    background = Image.new('RGBA', (width_max, height_max), (0, 0, 0, 255))
    font = ImageFont.truetype('./Ubuntu-Light.ttf', 20)
    

    data = ""
    i = 0
    
    offset_x = 7500
    offset_y = 1800
    
    for x in range(offset_x, offset_x + int(VIRT_DISPLAY_WIDTH / 6),  step):
        for y in range(offset_y, offset_y + int(VIRT_DISPLAY_HEIGHT / 6), step):
           
            ImageDraw.Draw(background).text(
                (x, y),
                f'{i:X}',
                (255,255,255),
                font=font)
            i += 1
            data += "{:X},{},{}\r\n".format(i, x, y)
    with open('convert.csv', 'w') as f:
        f.write(data)
    background = background.resize((REAL_DISPLAY_WIDTH, REAL_DISPLAY_HEIGHT), resample=Image.LANCZOS)
    background.save('1.png')
    

def combine_images(columns, space, images):

    width_max = VIRT_DISPLAY_WIDTH
    height_max = VIRT_DISPLAY_HEIGHT
    background = Image.new('RGBA', (width_max, height_max), (0, 0, 0, 255))
    
    # To move aruco down - increase y
    # To move aruco right - increase x
    
    
    aruco_boader_width = 7
    
    x, y = 10955, 6050
    img = Image.open(images[0])
    background_aruco = Image.new('RGBA', (img.width + aruco_boader_width, img.height + aruco_boader_width), (255, 255, 255, 255))
    background_aruco.paste(img, (aruco_boader_width // 2, aruco_boader_width // 2))
    background.paste(background_aruco, (x - aruco_boader_width // 2, y - aruco_boader_width // 2))
    
    
    x, y = 10930,1870  
    img = Image.open(images[1])
    background_aruco = Image.new('RGBA', (img.width + aruco_boader_width, img.height + aruco_boader_width), (255, 255, 255, 255))
    background_aruco.paste(img, (aruco_boader_width // 2, aruco_boader_width // 2))
    background.paste(background_aruco, (x - aruco_boader_width // 2, y - aruco_boader_width // 2))
    
    
    
    x, y = 7680,1880
    
    img = Image.open(images[2])
    background_aruco = Image.new('RGBA', (img.width + aruco_boader_width, img.height + aruco_boader_width), (255, 255, 255, 255))
    background_aruco.paste(img, (aruco_boader_width // 2, aruco_boader_width // 2))
    background.paste(background_aruco, (x - aruco_boader_width // 2, y - aruco_boader_width // 2))
    
    
    x, y = 7680, 6070
    
    img = Image.open(images[3])
    background_aruco = Image.new('RGBA', (img.width + aruco_boader_width, img.height + aruco_boader_width), (255, 255, 255, 255))
    background_aruco.paste(img, (aruco_boader_width // 2, aruco_boader_width // 2))
    background.paste(background_aruco, (x - aruco_boader_width // 2, y - aruco_boader_width // 2))
  
    
    background = background.resize((REAL_DISPLAY_WIDTH, REAL_DISPLAY_HEIGHT), resample=Image.LANCZOS)
    #enhancer = ImageEnhance.Brightness(background)
    #background = enhancer.enhance(0.22)
    background.save('1.png')

def generate_bulk_markers():
    #marker_size = 6
    marker_size = 30
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


def make_cross_markers():
    width_max = VIRT_DISPLAY_WIDTH
    height_max = VIRT_DISPLAY_HEIGHT
    background = Image.new('RGBA', (width_max, height_max), (0, 0, 0, 255))
    
    # To move aruco down - increase y
    # To move aruco right - increase x
    
    draw = ImageDraw.Draw(background)
    def draw_cross(x, y, size=25):
        draw.line((x + size, y, x - size, y), fill='white', width=2) 
        draw.line((x, y + size, x, y - size), fill='white', width=2) 
    
    #corrections should be minused from these values
    # top left corner, frame_0
    x, y = 10955 + 19, 6050 + 4
    draw_cross(x, y)
    
    # bottom left corner, frame_2
    x, y = 10930 + 14,1870 - 17  
    draw_cross(x, y);
    
    # Bottom right corner, frame 3
    x, y = 7680 + 1,1880 - 8
    draw_cross(x, y);
    
    # Top right corner, frame 1
    x, y = 7680 + 33, 6070 + 5
    draw_cross(x, y);

    background = background.resize((REAL_DISPLAY_WIDTH, REAL_DISPLAY_HEIGHT), resample=Image.LANCZOS)
    background.save('1.png')

#x = generate_bulk_markers()
#combine_images(columns=3, space=20, images=x)

make_cross_markers()
#generate_calibration_grid()
generate_chitubox_zip(None)
