import subprocess
import numpy as np
from generator import generate_chitubox_zip


DPI=2000
DPMM=2000/25.4
#DPMM=52.63157
REGISTRATION_DRILL_DIAMETER=2.0

OFFSET= DPMM * (REGISTRATION_DRILL_DIAMETER/2) # X and Y offset due to diameter of hole
registration_drill_coordinates_mm = [(0, 0), (62, 0), (0, 85), (62, 85)]


subprocess.call(['/usr/bin/gerbv', '-x', 'png', 
                 '-o', '/home/artsin/Dev/goofile_generator/result.png',
                 '-D', str(DPI),
                 '-B', '0',

                 '-m', 'X',
                 '/home/artsin/Dev/goofile_generator/gerbers/mix_reg_testboard/board_70x100_62x85drills_no_keys.drl', '-f#FFFFFFFF',
                 '/home/artsin/Dev/goofile_generator/gerbers/mix_reg+dcoboard/dioid-F_Cu.gbr', '-f#FFFFFFFF'
                 ])

registration_drill_coordinates_px = []
for coordinate in registration_drill_coordinates_mm:
    x_px, y_px = coordinate
    x_px *= DPMM
    y_px *= DPMM
    
    x_px += OFFSET
    y_px += OFFSET
    registration_drill_coordinates_px.append((x_px, y_px))
    

print(registration_drill_coordinates_px)

import json
real_coordinates = []
#real_coordinates = [(10953, 1584), (7689, 1606), (10982, 6054), (7714, 6073)]
with open('points.json', 'r') as openfile:
    real_coordinates = json.load(openfile)

print(real_coordinates)

import matplotlib.pyplot as plt

registration_drill_coordinates_px = np.array(registration_drill_coordinates_px)
real_coordinates = np.array(real_coordinates)
#plt.scatter(registration_drill_coordinates_px[:,0], registration_drill_coordinates_px[:, 1], c ="blue")
#plt.scatter(real_coordinates[:,0], real_coordinates[:, 1], c ="green")


from functools import partial
import matplotlib.pyplot as plt
#from pycpd import AffineRegistration, DeformableRegistration, RigidRegistration
import numpy as np
from cycpd import affine_registration, rigid_registration, deformable_registration

def visualize(iteration, error, X, Y, ax):
    plt.cla()
    ax.scatter(X[:, 0],  X[:, 1], color='green', label='Target')
    ax.scatter(Y[:, 0],  Y[:, 1], color='blue', label='Source')
    plt.text(0.87, 0.92, 'Iteration: {:d}\nQ: {:06.4f}'.format(
        iteration, error), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize='x-large')
    ax.legend(loc='upper left', fontsize='x-large')
    plt.draw()
    plt.pause(0.01)



Y = registration_drill_coordinates_px.astype('double')
X = real_coordinates.astype('double')

fig = plt.figure()
fig.add_axes([0, 0, 1, 1])
callback = partial(visualize, ax=fig.axes[0])

#reg_main = AffineRegistration(**{'X': X, 'Y': Y})
#reg_main.register(callback)

reg_main = affine_registration(**{'X': X, 'Y': Y})
reg_main.register(callback)

Y_corrected = reg_main.transform_point_cloud(Y)
reg_correction = deformable_registration(alpha=0.01, beta=0.1, num_eig=100000, **{'X': X, 'Y': Y_corrected})
reg_correction.register(callback)
Y_refined = reg_correction.transform_point_cloud(Y_corrected)
#Y = reg_correction.transform_point_cloud(Y)
#plt.show()
#print(X)
#print(Y)
#print(reg.get_registration_parameters())



import cv2
 
# To read image from disk, we use
# cv2.imread function, in below method,
img = cv2.imread("result.png", cv2.IMREAD_GRAYSCALE)


white_pixels = cv2.findNonZero(img)
Y_gerber = white_pixels[:, 0].astype('double')
Y_gerber_corrected = reg_main.transform_point_cloud(Y_gerber)
Y_gerber_refined = reg_correction.transform_point_cloud(Y_gerber_corrected)

import matplotlib.pyplot as plt

#plt.scatter(white_pixels[:, 0][:, 0], white_pixels[:, 0][:, 1])

plt.scatter(Y_gerber[:,0][::100], Y_gerber[:,1][::100])
plt.scatter(Y_gerber_corrected[:,0][::100], Y_gerber_corrected[:,1][::100])
plt.scatter(Y_gerber_refined[:,0][::100], Y_gerber_refined[:,1][::100])
plt.scatter(Y[:, 0],  Y[:, 1], color='red', marker=6, label='Target')
plt.scatter(Y_refined[:, 0],  Y_refined[:, 1], color='cyan', marker=11, label='Target')

# Generation of result imaage

PIXEL_RATIO = 24/19
REAL_DISPLAY_WIDTH = 11520
REAL_DISPLAY_HEIGHT = 5120
VIRT_DISPLAY_WIDTH = 11520
VIRT_DISPLAY_HEIGHT = int(REAL_DISPLAY_HEIGHT * PIXEL_RATIO)
print("Generating image")

import numpy as np
from PIL import Image

# Define the dimensions of the image
width = VIRT_DISPLAY_WIDTH  # Adjust as needed
height = VIRT_DISPLAY_HEIGHT  # Adjust as needed

image = np.zeros((height, width), dtype=np.uint8)
for x, y in Y_gerber_refined:
    image[int(y), int(x)] = 255  # Set the pixel to white (255)
pil_image = Image.fromarray(image)

pil_image = pil_image.resize((REAL_DISPLAY_WIDTH, REAL_DISPLAY_HEIGHT), resample=Image.LANCZOS)

pil_image.save('1.png')
generate_chitubox_zip(None)
