"""Command-line interface for ByakuganVisualizer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from byakuganvisualizer import __version__
from byakuganvisualizer.filters import FILTERS
from byakuganvisualizer.processor import ByakuganProcessor, ImagePair

__author__ = "HokageM"
__copyright__ = "HokageM"
__license__ = "MIT"


def parse_image_pairs(raw_value: str) -> list[ImagePair]:
    """Parse image pairs formatted as 'image1,image2;image3,image4'."""
    image_pairs: list[ImagePair] = []

    for raw_pair in raw_value.split(";"):
        paths = [part.strip() for part in raw_pair.split(",")]

        if len(paths) != 2 or not all(paths):
            raise argparse.ArgumentTypeError(
                f"Invalid image pair '{raw_pair}'. Expected format: image1,image2"
            )

        image_pairs.append((Path(paths[0]), Path(paths[1])))

    return image_pairs


def parse_image_list(raw_value: str) -> list[Path]:
    """Parse comma-separated image paths."""
    image_paths = [Path(part.strip()) for part in raw_value.split(",") if part.strip()]

    if not image_paths:
        raise argparse.ArgumentTypeError("At least one image path is required.")

    return image_paths


def parse_args(args: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "ByakuganVisualizer: correct color palettes for colorblind users "
            "and highlight differences between images."
        )
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"ByakuganVisualizer {__version__}",
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--diff",
        type=parse_image_pairs,
        help=(
            "Image pairs to compare, formatted as "
            "'Path_To_Image1a,Path_To_Image2a;Path_To_Image1b,Path_To_Image2b'."
        ),
    )
    mode.add_argument(
        "--images",
        type=parse_image_list,
        help="Comma-separated image paths to process, e.g. A.png,B.png,C.png.",
    )

    parser.add_argument(
        "--filter",
        dest="filter_name",
        choices=sorted(FILTERS),
        help="Optional RGB filter to apply.",
    )
    parser.add_argument(
        "--deuteranomaly",
        type=float,
        default=0.0,
        help="Degree of deuteranomaly correction. Default: 0.0.",
    )
    parser.add_argument(
        "--protanomaly",
        type=float,
        default=0.0,
        help="Degree of protanomaly correction. Default: 0.0.",
    )
    parser.add_argument(
        "--out-dir",
        "--out_dir",
        dest="out_dir",
        type=Path,
        default=Path("tests/test_images"),
        help="Output directory for generated images. Default: current directory.",
    )

    return parser.parse_args(args)


def main(args: list[str] | None = None) -> int:
    """Run the CLI."""
    parsed_args = parse_args(sys.argv[1:] if args is None else args)

    processor = ByakuganProcessor(
        out_dir=parsed_args.out_dir,
        filter_name=parsed_args.filter_name,
        deuteranomaly=parsed_args.deuteranomaly,
        protanomaly=parsed_args.protanomaly,
    )

    print("BYAKUGAN ACTIVATED!")

    if parsed_args.diff:
        output_paths = processor.calculate_diffs(parsed_args.diff)
    else:
        output_paths = processor.process_images(parsed_args.images)

    for output_path in output_paths:
        print(f"Saved: {output_path}")

    return 0


def run() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    run()
