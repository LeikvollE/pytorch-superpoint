import random

from utils.photometric_augmentation import vignette, add_snow


class Snow(object):

    def __init__(self):
        self.pixels_per_snow_max = 900
        self.pixels_per_snow_min = 700
        self.snow_max_size = 3
        self.snow_min_size = 1
        self.p = 0.6

    def __call__(self, image):
        return add_snow(image,
                        pixels_per_snow_max=self.pixels_per_snow_max,
                        pixels_per_snow_min=self.pixels_per_snow_min,
                        max_size=self.snow_max_size,
                        min_size=self.snow_min_size
                        ) if random.random() < self.p else image


class Vignette(object):

    def __init__(self):
        self.scale = 1.6
        self.p = 0.75

    def __call__(self, image):
        return vignette(image) if random.random() < self.p else image
