import numpy as np
import os

from PIL import Image

from byakuganvisualizer.ImageFilter import ImageFilter


class Byakugan:
    """
    This class is used to process images by applying filters and calculating differences between pairs of images.
    """

    def __init__(self, out_dir='.', filter='', deuteranomaly=0, protanomaly=0):
        self.out_dir = out_dir
        self.filter = filter
        self.protanomaly = protanomaly
        self.deuteranomaly = deuteranomaly

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def apply_filters(self, image_data):
        """
        Apply filters to the image data.
        :param image_data: The image data to apply the filters to.
        :return: Tuple consisting of filtered image data and the suffix representing the filters applied.
        """
        suffix = ''
        if self.filter == 'red':
            image_data = ImageFilter.apply_red_filter(image_data)
            suffix += '_red'
        if self.filter == 'blue':
            image_data = ImageFilter.apply_blue_filter(image_data)
            suffix += '_blue'
        if self.filter == 'green':
            image_data = ImageFilter.apply_green_filter(image_data)
            suffix += '_green'
        if self.filter == 'yellow':
            image_data = ImageFilter.apply_yellow_filter(image_data)
            suffix += '_yellow'
        if self.protanomaly > 0 or self.deuteranomaly > 0:
            image_data = ImageFilter.correction_for_colorblindness(image_data, self.protanomaly, self.deuteranomaly)
            suffix += f'_deuteranomaly_{self.deuteranomaly}_protanomaly_{self.protanomaly}'
        return image_data, suffix

    def calculate_diffs(self, diff_pairs):
        """
        Calculate the differences between pairs of images.
        :param diff_pairs:
        :return:
        """
        for pair in diff_pairs:
            pair_name = os.path.basename(pair[0]).split('.')[0] + '_' + os.path.basename(pair[1]).split('.')[0]
            file_extension_1 = os.path.basename(pair[0]).split('.')[1]
            file_extension_2 = os.path.basename(pair[1]).split('.')[1]

            if file_extension_1 != file_extension_2:
                raise ValueError(f"Images must have the same file extension. {file_extension_1} != {file_extension_2}")

            image1 = Image.open(pair[0])
            image2 = Image.open(pair[1])

            array1 = np.array(image1)
            array2 = np.array(image2)

            if array1.shape != array2.shape:
                raise ValueError(f"Images must be of the same size. {array1.shape} != {array2.shape}")

            difference_array = np.abs(array1 - array2)

            difference_array, suffix = self.apply_filters(difference_array)
            pair_name += suffix

            difference_image = Image.fromarray(difference_array.astype('uint8'))
            difference_image.save(f'{self.out_dir}/Diff_{pair_name}.{file_extension_1}')

    def process_images(self, images):
        """
        Process images by applying filters.
        :param images:
        :return:
        """
        for img in images:
            image_name, file_extension = os.path.basename(img).split('.')

            image = Image.open(img)
            rgb_array = np.array(image)

            rgb_array, suffix = self.apply_filters(rgb_array)
            image_name += suffix

            filtered_image = Image.fromarray(rgb_array.astype('uint8'))
            filtered_image.save(f'{self.out_dir}/Filtered_{image_name}.{file_extension}')
