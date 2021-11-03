import numpy as np
import random
import cv2

import cv2
import numpy as np
import math


# ============================================================================

def ellipse_bbox(h, k, a, b, theta):
    ux = a * math.cos(theta)
    uy = a * math.sin(theta)
    vx = b * math.cos(theta + math.pi / 2)
    vy = b * math.sin(theta + math.pi / 2)
    box_halfwidth = np.ceil(math.sqrt(ux ** 2 + vx ** 2))
    box_halfheight = np.ceil(math.sqrt(uy ** 2 + vy ** 2))
    return ((int(h - box_halfwidth), int(k - box_halfheight))
            , (int(h + box_halfwidth), int(k + box_halfheight)))


# Rotated elliptical gradient - faster, vectorized numpy approach
def make_gradient_v2(width, height, h, k, a, b, theta):
    # Precalculate constants
    st, ct = math.sin(theta), math.cos(theta)
    aa, bb = a ** 2, b ** 2

    # Generate (x,y) coordinate arrays
    y, x = np.mgrid[-k:height - k, -h:width - h]
    # Calculate the weight for each pixel
    weights = (((x * ct + y * st) ** 2) / aa) + (((x * st - y * ct) ** 2) / bb)

    return np.clip(1.0 - weights, 0, 1)

def draw_snow(a, b, theta, inner_scale, save_intermediate=False):
    # Calculate the image size needed to draw this and center the ellipse
    _, (h, k) = ellipse_bbox(0, 0, a, b, theta)  # Ellipse center
    h += 2  # Add small margin
    k += 2  # Add small margin
    width, height = (h * 2 + 1, k * 2 + 1)  # Canvas size

    # Generate the gradient and scale it to 8bit grayscale range
    intensity = np.uint8(make_gradient_v2(width, height, h, k, a, b, theta) * 255)

    # Turn it into a BGRA image
    result = cv2.merge([intensity, intensity, intensity])
    return result

def add_snow(img):
    # reading the image
    image = cv2.imread(img)

    # resizing the image according to our need resize() function takes 2 parameters,
    # the image and the dimensions

    # Extracting the height and width of an image
    rows, cols = image.shape[:2]

    snows = 50
    for i in range(snows):
        a, b = (random.randint(2, 6), random.randint(2, 6))  # Semi-major and semi-minor axis
        theta = math.radians(90.0 * random.random())  # Ellipse rotation (radians)

        snow = draw_snow(a, b, theta, True)
        # displaying the orignal image
        cv2.imshow('Original', snow)
        # displaying the vignette filter image
        cv2.waitKey(0)

    # displaying the orignal image
    cv2.imshow('Original', image)
    # displaying the vignette filter image
    #cv2.imshow('VIGNETTE', output)
    cv2.waitKey(0)

if __name__ == "__main__":
    add_snow('b737.jpg')
"""
    snow('0.png')
    snow('0.png')
    snow('0.png')
    snow('0.png')

    snow('1.png')
    snow('1.png')
    snow('1.png')
    snow('1.png')

    snow('2.png')
    snow('2.png')
    snow('2.png')
    snow('2.png')

    snow('3.png')
    snow('3.png')
    snow('3.png')
    snow('3.png')
"""
