#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:42:02 2023
@author: artsin
"""
import os
import zipfile
import cv2
import yaml
import argparse


with open("config.cfg") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
    
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
    zf.close()


from PIL import Image, ImageFont, ImageDraw

def generate_calibration_grid():
    width_max = VIRT_DISPLAY_WIDTH
    height_max = VIRT_DISPLAY_HEIGHT
    step = 60
    background = Image.new('RGBA', (width_max, height_max), (0, 0, 0, 255))
    font = ImageFont.truetype('./misc/Ubuntu-Light.ttf', 20)
    
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
    

def make_cross_markers(use_corrections=False):
    width_max = VIRT_DISPLAY_WIDTH
    height_max = VIRT_DISPLAY_HEIGHT
    background = Image.new('RGBA', (width_max, height_max), (0, 0, 0, 255))
    
    # To move aruco down - increase y
    # To move aruco right - increase x
    
    draw = ImageDraw.Draw(background)
    def draw_cross(x, y, size=25):
        draw.line((x + size, y, x - size, y), fill='white', width=2) 
        draw.line((x, y + size, x, y - size), fill='white', width=2) 
    
    # Corrections should be minused from these values
    # top left corner, frame_0
    
    frames = ["frame_0", "frame_1", "frame_2", "frame_3"]
    if use_corrections:
        corrections = read_corrections()
        print(">>>> Correction read: ", corrections)
    for frame in frames:
        if use_corrections:
            draw_cross(cfg[frame]["x"] - corrections[frame + ".jpg"][0], cfg[frame]["y"] - corrections[frame + ".jpg"][1])
        else:
            draw_cross(cfg[frame]["x"], cfg[frame]["y"])
    

    background = background.resize((REAL_DISPLAY_WIDTH, REAL_DISPLAY_HEIGHT), resample=Image.LANCZOS)
    background.save('1.png')


def read_corrections():
    import csv
    
    corrections = dict()
    with open('corrections.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            corrections[line['frame'] ]= (int(line['correction_x']), int(line['correction_y']))
    
    return corrections

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate files running on LUCID lithomachine')
    parser.add_argument("--correct", action="store_true", help='Read and use registration point corrections from file')
    parser.add_argument("--grid", action="store_true", help='Generate rought numeric grid for initial positioning')
    args = parser.parse_args()

    make_cross_markers(args.correct)

    if args.grid:
        generate_calibration_grid()
        
    generate_chitubox_zip(None)

