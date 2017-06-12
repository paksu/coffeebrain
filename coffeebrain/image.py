import numpy as np
from StringIO import StringIO
from PIL import Image

DOWNSIZED_IMAGE_SIZE = (75, 75)


def process_image(image_path=None, image_data=None):
    """
    Processes the given image at path or buffer so it can be used for prediction

    Returns a tuple of (left, right) that contain numpy arrays that can be fed to SVC
    """
    assert image_path or image_data, "Either image_path or image_data must be given"
    # Load the image data and contert it to greyscale
    image = Image.open(image_path or StringIO(image_data)).convert('L')

    # Crop the image and split in into left and right sides so each pot can be predicted separately
    width, height = image.size
    downsized_left = image.crop((0, 0, width / 2, height)).resize(DOWNSIZED_IMAGE_SIZE)
    downsized_right = image.crop((width / 2, 0, width, height)).resize(DOWNSIZED_IMAGE_SIZE)

    # Return two numpy arrays (feature vectors) for both sides of the data
    return np.array(downsized_left).flatten(), np.array(downsized_right).flatten()
