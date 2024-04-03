import argparse
import sys
import os

from byakuganvisualizer import __version__
from byakuganvisualizer.Byakugan import Byakugan

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

    if args.diff is None and args.images is None:
        print("No images to process.")
        return

    if args.diff and args.images:
        raise ValueError("Please do not use --diff and --images at the same time.")

    with Byakugan(args.out_dir, args.filter, args.deuteranomaly, args.protanomaly) as byakugan:
        print("BYAKUGAN ACTIVATED!")
        if args.diff:
            byakugan.calculate_diffs(args.diff)
        if args.images:
            args.images = args.images.split(',')
            byakugan.process_images(args.images)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
