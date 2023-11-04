#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 11:21:43 2023

@author: artsin
"""
from PIL import Image

# Open your two images
image1 = Image.open('1.png')
image2 = Image.open('2.png')

# Ensure both images have the same size
#image2 = image2.resize(image1.size)

# Convert all white pixels in image1 to blue
image1 = image1.convert('RGBA')
data = image1.getdata()
new_data = []
for item in data:
    if item[:3] == (255, 255, 255):
        new_data.append((0, 0, 255, 0))  # Convert white pixels to blue (RGBA format)
    elif item[:3] == (0, 0, 0):
        new_data.append((0, 0, 0, 0))  # Convert white pixels to blue (RGBA format)
    else:
        new_data.append(item)
image1.putdata(new_data)

# Composite the modified image1 over image2
result = Image.alpha_composite(image2.convert('RGBA'), image1)

# Save the final image
result.save('output.png')
