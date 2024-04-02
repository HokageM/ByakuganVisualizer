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
        red_filtered[:, :, 0] = image_data[:, :, 0]
        return red_filtered

    @staticmethod
    def apply_green_filter(image_data):
        """
        Apply a green filter to the image data. This will double the green channel values.
        :param image_data: The image data to apply the filter to.
        """
        green_filtered = np.zeros_like(image_data)
        green_filtered[:, :, 1] = image_data[:, :, 1]
        return green_filtered

    @staticmethod
    def apply_blue_filter(image_data):
        """
        Apply a blue filter to the image data. This will double the blue channel values.
        :param image_data:
        :return:
        """
        blue_filtered = np.zeros_like(image_data)
        blue_filtered[:, :, 2] = image_data[:, :, 2]
        return blue_filtered

    @staticmethod
    def apply_yellow_filter(image_data):
        """
        Apply a yellow filter to the image data. This will double the red and green channel values.
        :param image_data:
        :return:
        """
        yellow_filtered = np.zeros_like(image_data)
        yellow_filtered[:, :, 0] = image_data[:, :, 0]
        yellow_filtered[:, :, 1] = image_data[:, :, 1]
        return yellow_filtered

    @staticmethod
    def correction_for_colorblindness(image_array, degree_protanomaly, degree_deuteranomaly):
        """
        Apply a colorblindness correction to the image data.
        :param image_array:
        :param degree_protanomaly:
        :param degree_deuteranomaly:
        :return:
        """
        r = image_array[..., 0]
        g = image_array[..., 1]
        b = image_array[..., 2]

        corrected = np.copy(image_array)
        r_corrected = (1 - degree_deuteranomaly / 2) * r + (degree_deuteranomaly / 2) * g
        g_corrected = (degree_protanomaly / 2) * r + (1 - degree_protanomaly / 2) * g
        b_corrected = ((degree_protanomaly / 4) * r + (degree_deuteranomaly / 4) * g +
                       (1 - (degree_deuteranomaly + degree_protanomaly) / 4) * b)

        corrected[..., 0] = r_corrected
        corrected[..., 1] = g_corrected
        corrected[..., 2] = b_corrected
        return corrected
