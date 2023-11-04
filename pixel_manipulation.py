#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:20:52 2023

@author: artsin
"""

# Python code to read image
import cv2
 
# To read image from disk, we use
# cv2.imread function, in below method,
img = cv2.imread("result.png", cv2.IMREAD_GRAYSCALE)


white_pixels = cv2.findNonZero(img)

import matplotlib.pyplot as plt

plt.scatter(white_pixels[:, 0][:, 0], white_pixels[:, 0][:, 1])
# Creating GUI window to display an image on screen
# first Parameter is windows title (should be in string format)
# Second Parameter is image array
#cv2.imshow("image", img)
 
# To hold the window on screen, we use cv2.waitKey method
# Once it detected the close input, it will release the control
# To the next line
# First Parameter is for holding screen for specified milliseconds
# It should be positive integer. If 0 pass an parameter, then it will
# hold the screen until user close it.
#cv2.waitKey(0)
 
# It is for removing/deleting created GUI window from screen
# and memory
#cv2.destroyAllWindows()
