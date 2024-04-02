import argparse
import sys
import numpy as np
import os

from PIL import Image

from byakuganvisualizer import __version__
from byakuganvisualizer.ImageFilter import ImageFilter

__author__ = "HokageM"
__copyright__ = "HokageM"
__license__ = "MIT"


def parse_tuples(tuples_str):
    """
    Parse a string containing a list of tuples.
    :param tuples_str:
    :return:
    """
    tuples_list = []
    for pair in tuples_str.split(';'):
        if ',' in pair:
            tuple_pair = tuple(pair.split(','))
            tuples_list.append(tuple_pair)
        else:
            print("Invalid tuple format:", pair)
            return None
    return tuples_list


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="ByakuganVisualizer: Tool for correcting the color palett for color blind people and highlighting "
                    "differences of images."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"ByakuganVisualizer {__version__}",
    )
    parser.add_argument(
        '--diff',
        type=parse_tuples,
        help='String containing a list of tuples "Path_To_Image1a,Path_To_Image2a;Path_To_Image1b,Path_To_Image2b...". '
             'Each tuple contains two paths to images to be compared.'
    )
    parser.add_argument(
        '--filter',
        choices=['red', 'blue', 'green', 'yellow'],
        help='Filter type (red, blue, green, yellow)'
    )
    parser.add_argument(
        '--images',
        type=str,
        help='List of image names to be manipulated by a filter. E.g.: A,B,C,D'
    )
    parser.add_argument(
        '--deuteranomaly',
        type=float,
        default=0,
        help='Expresses your degree of deuteranomaly, which will be used to correct the image. Default is 1.'
    )
    parser.add_argument(
        '--protanomaly',
        type=float,
        default=0,
        help='Expresses your degree of protanomaly, which will be used to correct the image. Default is 1.'
    )
    parser.add_argument(
        '--out_dir',
        type=str,
        default='.',
        help='Output directory for the difference images'
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
        print(f"Output Directory: '{args.out_dir}' created.")

    if args.diff:
        for pair in args.diff:
            pair_name = os.path.basename(pair[0]).split('.')[0] + '_' + os.path.basename(pair[1]).split('.')[0]

            image1 = Image.open(pair[0])
            image2 = Image.open(pair[1])

            array1 = np.array(image1)
            array2 = np.array(image2)

            # Calculate the absolute difference between the two arrays
            difference_array = np.abs(array1 - array2)

            if args.filter == 'red':
                difference_array = ImageFilter.apply_red_filter(difference_array)
                pair_name += '_red'
            if args.filter == 'blue':
                difference_array = ImageFilter.apply_blue_filter(difference_array)
                pair_name += '_blue'
            if args.filter == 'green':
                difference_array = ImageFilter.apply_green_filter(difference_array)
                pair_name += '_green'
            if args.filter == 'yellow':
                difference_array = ImageFilter.apply_yellow_filter(difference_array)
                pair_name += '_yellow'

            difference_image = Image.fromarray(difference_array.astype('uint8'))
            difference_image.save(f'{args.out_dir}/Diff_{pair_name}.jpg')

    if args.images:
        args.images = args.images.split(',')
        for img in args.images:
            image_name = os.path.basename(img).split('.')[0]

            image = Image.open(img)
            rgb_array = np.array(image)

            if args.filter == 'red':
                rgb_array = ImageFilter.apply_red_filter(rgb_array)
                image_name += '_red'
            if args.filter == 'blue':
                rgb_array = ImageFilter.apply_blue_filter(rgb_array)
                image_name += '_blue'
            if args.filter == 'green':
                rgb_array = ImageFilter.apply_green_filter(rgb_array)
                image_name += '_green'
            if args.filter == 'yellow':
                rgb_array = ImageFilter.apply_yellow_filter(rgb_array)
                image_name += '_yellow'
            if args.protanomaly > 0 or args.deuteranomaly > 0:
                rgb_array = ImageFilter.correction_for_colorblindness(rgb_array, args.protanomaly, args.deuteranomaly)
                image_name += f'_deuteranomaly_{args.deuteranomaly}_protanomaly_{args.protanomaly}'

            filtered_image = Image.fromarray(rgb_array.astype('uint8'))
            filtered_image.save(f'{args.out_dir}/Filtered_{image_name}.jpg')


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
