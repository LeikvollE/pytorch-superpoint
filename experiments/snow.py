import random

import cv2
import numpy as np
import math

def ellipse_bbox(h, k, a, b, theta):
    ux = a * math.cos(theta)
    uy = a * math.sin(theta)
    vx = b * math.cos(theta + math.pi / 2)
    vy = b * math.sin(theta + math.pi / 2)
    box_halfwidth = np.ceil(math.sqrt(ux ** 2 + vx ** 2))
    box_halfheight = np.ceil(math.sqrt(uy ** 2 + vy ** 2))
    return (int(h + box_halfwidth), int(k + box_halfheight))


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

def draw_snow(a, b, theta, channels):
    # Calculate the image size needed to draw this and center the ellipse
    (h, k) = ellipse_bbox(0, 0, a, b, theta)  # Ellipse center

    width, height = (h * 2, k * 2)  # Canvas size

    # Generate the gradient and scale it to 8bit grayscale range
    intensity = np.uint8(make_gradient_v2(width, height, h, k, a, b, theta) * 255 * (0.2 + random.random() * 0.8))

    # Turn it into a BGRA image
    result = cv2.merge([intensity] * channels)
    return result

def add_snow(img, pixels_per_snow_max=900, pixels_per_snow_min=700, max_size=3, min_size=1):
    # reading the image
    image = cv2.imread(img)

    # resizing the image according to our need resize() function takes 2 parameters,
    # the image and the dimensions

    # Extracting the height and width of an image
    rows, cols, channels = image.shape

    area = rows * cols
    snows = area // random.randint(pixels_per_snow_min, pixels_per_snow_max)

    output = image.copy()
    for _ in range(snows):
        a, b = (random.randint(min_size, max_size), random.randint(min_size, max_size))  # Semi-major and semi-minor axis
        theta = math.radians(90.0 * random.random())  # Ellipse rotation (radians)

        snow = draw_snow(a, b, theta, channels)

        # displaying the orignal image
        x, y = random.randint(0, cols - snow.shape[1]), random.randint(0, rows - snow.shape[0])
        w = np.ones_like(snow)

        weighted_square = output[y:y + snow.shape[0], x:x + snow.shape[1], :] * (w - snow/255)
        output[y:y + snow.shape[0], x:x + snow.shape[1], :] = np.add(weighted_square.astype(np.uint8), snow, dtype=np.uint8)

    print(np.max(image))
    # displaying the orignal image
    cv2.imshow('Original', image)
    # displaying the vignette filter image
    cv2.imshow('VIGNETTE', output)
    cv2.waitKey(0)

if __name__ == "__main__":
    add_snow('0.png')
    add_snow('0.png')
    add_snow('0.png')
    add_snow('0.png')

    add_snow('1.png')
    add_snow('1.png')
    add_snow('1.png')
    add_snow('1.png')

    add_snow('2.png')
    add_snow('2.png')
    add_snow('2.png')
    add_snow('2.png')

    add_snow('3.png')
    add_snow('3.png')
    add_snow('3.png')
    add_snow('3.png')
