""" deprecated: photometric augmentation from tensorflow implementation
# not used in our pipeline
# need to verify if synthetic generation uses it.
"""
import math
import random

import cv2
import cv2 as cv
import numpy as np
import tensorflow as tf


augmentations = [
        'additive_gaussian_noise',
        'additive_speckle_noise',
        'random_brightness',
        'random_contrast',
        'additive_shade',
        'motion_blur'
]

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
    min = np.min(weights)

    return np.clip((1.0 - weights)/(1 - min), 0, 1)

def draw_snow(a, b, theta):
    # Calculate the image size needed to draw this and center the ellipse
    (h, k) = ellipse_bbox(0, 0, a, b, theta)  # Ellipse center
    width, height = (h * 2, k * 2)  # Canvas size

    # Generate the gradient and scale it to 8bit grayscale range
    intensity = make_gradient_v2(width, height, h, k, a, b, theta)
    return intensity * (0.15 + random.random() * 0.85)

def add_snow(image, pixels_per_snow_max=900, pixels_per_snow_min=700, max_size=3, min_size=1):

    # Extracting the height and width of an image
    rows, cols = image.shape[:2]

    area = rows * cols
    snows = area // random.randint(pixels_per_snow_min, pixels_per_snow_max)
    for _ in range(snows):
        a, b = (random.randint(min_size, max_size), random.randint(min_size, max_size))  # Semi-major and semi-minor axis
        theta = math.radians(90.0 * random.random())  # Ellipse rotation (radians)

        snow = draw_snow(a, b, theta)

        # displaying the orignal image
        x, y = random.randint(0, cols - snow.shape[1]), random.randint(0, rows - snow.shape[0])
        w = np.ones_like(snow)

        weighted_square = image[y:y + snow.shape[0], x:x + snow.shape[1], 0] * (w - snow)
        image[y:y + snow.shape[0], x:x + snow.shape[1], 0] = weighted_square + snow

    return image


def vignette(image):
    rows, cols = image.shape[:2]

    # generating vignette mask using Gaussian resultant_kernels
    sigma_X = cols / (1.5 + random.random() * 1.5)
    sigma_Y = rows / (1.5 + random.random() * 1.5)

    scale = 1.6
    X_resultant_kernel = cv2.getGaussianKernel(int(scale * cols), sigma_X)
    Y_resultant_kernel = cv2.getGaussianKernel(int(scale * rows), sigma_Y)

    start_X = random.randint(0, int(scale * cols) - cols)
    start_Y = random.randint(0, int(scale * rows) - rows)

    X_resultant_kernel = X_resultant_kernel[start_X:start_X + cols]
    Y_resultant_kernel = Y_resultant_kernel[start_Y:start_Y + rows]

    # generating resultant_kernel matrix
    resultant_kernel = Y_resultant_kernel * X_resultant_kernel.T

    # creating mask and normalising by using np.linalg function

    mask = resultant_kernel * (random.random() * 0.3 + 0.7) / np.max(resultant_kernel)
    image[:, :, 0] = image[:, :, 0] * mask
    return image


def additive_gaussian_noise(image, stddev_range=[5, 95]):
    stddev = tf.random_uniform((), *stddev_range)
    noise = tf.random_normal(tf.shape(image), stddev=stddev)
    noisy_image = tf.clip_by_value(image + noise, 0, 255)
    return noisy_image


def additive_speckle_noise(image, prob_range=[0.0, 0.005]):
    prob = tf.random_uniform((), *prob_range)
    sample = tf.random_uniform(tf.shape(image))
    noisy_image = tf.where(sample <= prob, tf.zeros_like(image), image)
    noisy_image = tf.where(sample >= (1. - prob), 255.*tf.ones_like(image), noisy_image)
    return noisy_image


def random_brightness(image, max_abs_change=50):
    return tf.clip_by_value(tf.image.random_brightness(image, max_abs_change), 0, 255)


def random_contrast(image, strength_range=[0.5, 1.5]):
    return tf.clip_by_value(tf.image.random_contrast(image, *strength_range), 0, 255)


def additive_shade(image, nb_ellipses=20, transparency_range=[-0.5, 0.8],
                   kernel_size_range=[250, 350]):

    def _py_additive_shade(img):
        min_dim = min(img.shape[:2]) / 4
        mask = np.zeros(img.shape[:2], np.uint8)
        for i in range(nb_ellipses):
            ax = int(max(np.random.rand() * min_dim, min_dim / 5))
            ay = int(max(np.random.rand() * min_dim, min_dim / 5))
            max_rad = max(ax, ay)
            x = np.random.randint(max_rad, img.shape[1] - max_rad)  # center
            y = np.random.randint(max_rad, img.shape[0] - max_rad)
            angle = np.random.rand() * 90
            cv.ellipse(mask, (x, y), (ax, ay), angle, 0, 360, 255, -1)

        transparency = np.random.uniform(*transparency_range)
        kernel_size = np.random.randint(*kernel_size_range)
        if (kernel_size % 2) == 0:  # kernel_size has to be odd
            kernel_size += 1
        mask = cv.GaussianBlur(mask.astype(np.float32), (kernel_size, kernel_size), 0)
        shaded = img * (1 - transparency * mask[..., np.newaxis]/255.)
        return np.clip(shaded, 0, 255)

    shaded = tf.py_func(_py_additive_shade, [image], tf.float32)
    res = tf.reshape(shaded, tf.shape(image))
    return res


def motion_blur(image, max_kernel_size=10):

    def _py_motion_blur(img):
        # Either vertial, hozirontal or diagonal blur
        mode = np.random.choice(['h', 'v', 'diag_down', 'diag_up'])
        ksize = np.random.randint(0, (max_kernel_size+1)/2)*2 + 1  # make sure is odd
        center = int((ksize-1)/2)
        kernel = np.zeros((ksize, ksize))
        if mode == 'h':
            kernel[center, :] = 1.
        elif mode == 'v':
            kernel[:, center] = 1.
        elif mode == 'diag_down':
            kernel = np.eye(ksize)
        elif mode == 'diag_up':
            kernel = np.flip(np.eye(ksize), 0)
        var = ksize * ksize / 16.
        grid = np.repeat(np.arange(ksize)[:, np.newaxis], ksize, axis=-1)
        gaussian = np.exp(-(np.square(grid-center)+np.square(grid.T-center))/(2.*var))
        kernel *= gaussian
        kernel /= np.sum(kernel)
        img = cv.filter2D(img, -1, kernel)
        return img

    blurred = tf.py_func(_py_motion_blur, [image], tf.float32)
    return tf.reshape(blurred, tf.shape(image))
