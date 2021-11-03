import numpy as np
import random
import cv2


def vignette(img):
    # reading the image
    image = cv2.imread(img)

    # resizing the image according to our need resize() function takes 2 parameters,
    # the image and the dimensions

    # Extracting the height and width of an image
    rows, cols = image.shape[:2]

    # generating vignette mask using Gaussian resultant_kernels
    sigma_X = cols/(1.5 + random.random()*1.5)
    sigma_Y = rows/(1.5 + random.random()*1.5)

    scale = 1.6
    X_resultant_kernel = cv2.getGaussianKernel(int(scale * cols), sigma_X)
    Y_resultant_kernel = cv2.getGaussianKernel(int(scale * rows), sigma_Y)

    start_X = random.randint(0, int(scale * cols) - cols)
    start_Y = random.randint(0, int(scale * rows) - rows)

    X_resultant_kernel = X_resultant_kernel[start_X:start_X+cols]
    Y_resultant_kernel = Y_resultant_kernel[start_Y:start_Y+rows]
    np.reshape(X)

    # generating resultant_kernel matrix
    resultant_kernel = Y_resultant_kernel * X_resultant_kernel.T
    print(resultant_kernel.shape)

    # creating mask and normalising by using np.linalg function

    mask = resultant_kernel * (random.random() * 0.3 + 0.7) / np.max(resultant_kernel),
    output = np.copy(image)
    # applying the mask to each channel in the input image
    for i in range(3):
        output[:, :, i] = output[:, :, i] * mask
    # displaying the orignal image
    cv2.imshow('Original', image)
    # displaying the vignette filter image
    cv2.imshow('VIGNETTE', output)
    cv2.waitKey(0)

if __name__ == "__main__":
    vignette('0.png')
    vignette('0.png')
    vignette('0.png')
    vignette('0.png')

    vignette('1.png')
    vignette('1.png')
    vignette('1.png')
    vignette('1.png')

    vignette('2.png')
    vignette('2.png')
    vignette('2.png')
    vignette('2.png')

    vignette('3.png')
    vignette('3.png')
    vignette('3.png')
    vignette('3.png')

