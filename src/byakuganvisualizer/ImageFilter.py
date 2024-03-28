import numpy as np


class ImageFilter:
    """
    Class to apply filters to images.
    """

    @staticmethod
    def apply_red_filter(image_data):
        """
        Apply a red filter to the image data. This will double the red channel values.
        :param image_data:
        :return:
        """
        red_filtered = np.zeros_like(image_data)
        red_filtered[:, :, 0] = image_data[:, :, 0] * 2
        return red_filtered

    @staticmethod
    def apply_green_filter(image_data):
        """
        Apply a green filter to the image data. This will double the green channel values.
        :param image_data: The image data to apply the filter to.
        """
        green_filtered = np.zeros_like(image_data)
        green_filtered[:, :, 1] = image_data[:, :, 1] * 2
        return green_filtered

    @staticmethod
    def apply_blue_filter(image_data):
        """
        Apply a blue filter to the image data. This will double the blue channel values.
        :param image_data:
        :return:
        """
        blue_filtered = np.zeros_like(image_data)
        blue_filtered[:, :, 2] = image_data[:, :, 2] * 2
        return blue_filtered

    @staticmethod
    def apply_yellow_filter(image_data):
        """
        Apply a yellow filter to the image data. This will double the red and green channel values.
        :param image_data:
        :return:
        """
        yellow_filtered = np.zeros_like(image_data)
        yellow_filtered[:, :, 0] = image_data[:, :, 0] * 2
        yellow_filtered[:, :, 1] = image_data[:, :, 1] * 2
        return yellow_filtered
