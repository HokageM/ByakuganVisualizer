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
        description="ByakuganVisualizer: Tool for comparing images and highlighting differences."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"ByakuganVisualizer {__version__}",
    )
    parser.add_argument(
        '--diff',
        type=parse_tuples,
        required=True,
        help='String containing a list of tuples "Path_To_Image1a,Path_To_Image2a;Path_To_Image1b,Path_To_Image2b...". '
             'Each tuple contains two paths to images to be compared.'
    )
    parser.add_argument(
        '--filter',
        choices=['red', 'blue', 'green', 'yellow'],
        help='Filter type (red, blue, green, yellow)'
    )
    parser.add_argument(
        '--out_dir',
        type=str,
        default='.',
        help='Output directory for the difference images'
    )
    # TODO: option for just filtering an image
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
        print(f"Output Directory: '{args.out_dir}' created.")

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


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
