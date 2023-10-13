#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 14:54:31 2023

@author: artsin
"""


import cv2
import numpy as np
from matplotlib import pyplot as plt
import csv


def detect_cross(image, debug=False):
    img2 = image.copy()
    template = cv2.imread('./misc/template.png', cv2.IMREAD_GRAYSCALE)
    assert template is not None, "file could not be read, check with os.path.exists()"
    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    # methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']


    img = img2.copy()
    method = eval('cv2.TM_SQDIFF_NORMED')
    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    if debug:
        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        plt.subplot(121),plt.imshow(res, cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.show()
    
    return top_left[0] + w // 2, top_left[1] + h // 2


def detect_cirle(image, min_radius=140, max_radius=160, debug=False):
    
    image_circles = image.copy()
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    image_circles = clahe.apply(image_circles)
    #ret,image_circles = cv2.threshold(img_source,127,255,cv2.THRESH_BINARY)
    image_circles = cv2.GaussianBlur(image_circles, (25, 25), cv2.BORDER_DEFAULT)
    
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(
        image_circles,
        cv2.HOUGH_GRADIENT,
        3,
        2000,
        param1=70,  # the sensitivity; how strong the edges of the circles need to be. Too high and it won't detect anything, too low and it will find too much clutter.
        param2=70, # how many edge points it needs to find to declare that it's found a circle. Again, too high will detect nothing, too low will declare anything to be a circle.
        minRadius=min_radius,
        maxRadius=max_radius,
    )
    
    if detected_circles is not None:
    
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
    
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
    
            # Draw the circumference of the circle.
            cv2.circle(image_circles, (a, b), r, (0, 255, 0), 2)
            
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(image_circles, (a, b), 1, (0, 0, 255), 3)
            print(r)
        if debug:
            
            cv2.imshow("Detected Circle", image_circles)
            cv2.waitKey(0)
        return (a, b, r)


def calculate_corrections(cross_data, hole_data):
    # Correction params
    REAL_HOLE_DIAM = 2 # In mm
    DISPLAY_RESOLUTION_X = 0.019 # In mm
    DISPLAY_RESOLUTION_Y = 0.024 # In mm
    
    
    cross_x, cross_y = cross_data
    hole_x, hole_y, hole_r = hole_data
    
    # Get resolution in pixels per mm, knowing real diameter of hole
    PPMM = REAL_HOLE_DIAM / (hole_r * 2)
    corr_x = int(PPMM * (cross_x - hole_x) / DISPLAY_RESOLUTION_X)
    corr_y = int(PPMM * (cross_y - hole_y) / DISPLAY_RESOLUTION_Y)
    
    return corr_x, corr_y
    
    
    
def run():
    basedir = "/home/artsin/Dev/goofile_generator/camera_frames/"
    images = ["frame_0.jpg", "frame_1.jpg", "frame_2.jpg", "frame_3.jpg"]
    
    CORRECTION_FILE = 'corrections.csv'
    with open(CORRECTION_FILE, 'w') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["frame", "correction_x", "correction_y"])
        
        
    fig, axs = plt.subplots(2, 2)
    axs = axs.reshape(-1)
    for i, image in enumerate(images):
        ax = axs[i]
        
        img_source = cv2.imread(basedir + image, cv2.IMREAD_GRAYSCALE)
        cross_x, cross_y = detect_cross(img_source)
        hole_x, hole_y, hole_r = detect_cirle(img_source)
        corr_x, corr_y = calculate_corrections((cross_x, cross_y), (hole_x, hole_y, hole_r))
        print("-----------", image, "--------------")
        print("Detected cross: ", cross_x, cross_y)
        print("Detected hole: ", hole_x, hole_y, hole_r)
        print("Corrections", corr_x, corr_y)
        with open(CORRECTION_FILE, 'a') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow([image, corr_x, corr_y])
        
        # Show results
        ax.imshow(img_source)
        
        angle = np.linspace( 0 , 2 * np.pi , 150 ) 
        x = hole_x + hole_r * np.cos( angle ) 
        y = hole_y + hole_r * np.sin( angle ) 
        ax.plot(x, y, linewidth=3, color='red')
        ax.plot([hole_x - hole_r / 2, hole_x + hole_r / 2], [hole_y, hole_y], color='red')
        ax.plot([hole_x, hole_x], [hole_y - hole_r / 2, hole_y + hole_r / 2], color='red')
        
        
        ax.plot([cross_x - 10, cross_x + 10], [cross_y, cross_y], color='blue')
        ax.plot([cross_x, cross_x], [cross_y - 10, cross_y + 10], color='blue')
    
    plt.show()
    
if __name__ == '__main__':
    run()