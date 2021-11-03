from utils.photometric_augmentation import vignette


class Vignette(object):
    """Rescale the image in a sample to a given size.

    Args:
        output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
    """

    def __init__(self):
        self.scale = 1.6

    def __call__(self, image):
        return vignette(image)

