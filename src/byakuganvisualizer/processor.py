"""Core image-processing logic for ByakuganVisualizer."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import numpy as np
from PIL import Image

from byakuganvisualizer.filters import FILTERS, correction_for_colorblindness

PathLike = str | Path
ImagePair = tuple[PathLike, PathLike]


class ByakuganProcessor:
    """Apply RGB filters, colorblindness correction, and image diffs."""

    def __init__(
        self,
        out_dir: PathLike = ".",
        filter_name: str | None = None,
        deuteranomaly: float = 0.0,
        protanomaly: float = 0.0,
    ) -> None:
        if filter_name is not None and filter_name not in FILTERS:
            valid_filters = ", ".join(sorted(FILTERS))
            raise ValueError(
                f"Unknown filter '{filter_name}'. Valid filters are: {valid_filters}."
            )

        if deuteranomaly < 0 or protanomaly < 0:
            raise ValueError("deuteranomaly and protanomaly must be >= 0.")

        self.out_dir = Path(out_dir)
        self.filter_name = filter_name
        self.deuteranomaly = deuteranomaly
        self.protanomaly = protanomaly

        self.out_dir.mkdir(parents=True, exist_ok=True)

    def apply_filters(self, image_data: np.ndarray) -> tuple[np.ndarray, str]:
        """Apply the configured filter and colorblindness correction.

        Returns the transformed image array and the suffix used for output files.
        """
        suffix_parts: list[str] = []

        if self.filter_name:
            image_data = FILTERS[self.filter_name](image_data)
            suffix_parts.append(self.filter_name)

        if self.protanomaly > 0 or self.deuteranomaly > 0:
            image_data = correction_for_colorblindness(
                image_data,
                degree_protanomaly=self.protanomaly,
                degree_deuteranomaly=self.deuteranomaly,
            )
            suffix_parts.append(
                f"deuteranomaly_{self.deuteranomaly}_protanomaly_{self.protanomaly}"
            )

        suffix = f"_{'_'.join(suffix_parts)}" if suffix_parts else ""
        return image_data, suffix

    def process_images(self, image_paths: Iterable[PathLike]) -> list[Path]:
        """Process multiple images and return their output paths."""
        return [self.process_image(image_path) for image_path in image_paths]

    def process_image(self, image_path: PathLike) -> Path:
        """Process one image and save the filtered output image."""
        image_path = Path(image_path)
        image_array = self._read_rgb_array(image_path)

        filtered_array, suffix = self.apply_filters(image_array)

        output_path = (
            self.out_dir / f"Filtered_{image_path.stem}{suffix}{image_path.suffix}"
        )
        self._save_rgb_array(filtered_array, output_path)
        return output_path

    def calculate_diffs(self, image_pairs: Iterable[ImagePair]) -> list[Path]:
        """Calculate diffs for multiple image pairs and return output paths."""
        return [self.calculate_diff(first, second) for first, second in image_pairs]

    def calculate_diff(self, first_path: PathLike, second_path: PathLike) -> Path:
        """Calculate the absolute pixel difference between two images."""
        first_path = Path(first_path)
        second_path = Path(second_path)

        self._validate_matching_extensions(first_path, second_path)

        first_array = self._read_rgb_array(first_path)
        second_array = self._read_rgb_array(second_path)

        if first_array.shape != second_array.shape:
            raise ValueError(
                f"Images must be the same size: {first_array.shape} != {second_array.shape}."
            )

        diff_array = np.abs(
            first_array.astype(np.int16) - second_array.astype(np.int16)
        ).astype(np.uint8)

        diff_array, suffix = self.apply_filters(diff_array)

        pair_name = f"{first_path.stem}_{second_path.stem}{suffix}"
        output_path = self.out_dir / f"Diff_{pair_name}{first_path.suffix}"
        self._save_rgb_array(diff_array, output_path)
        return output_path

    @staticmethod
    def _read_rgb_array(image_path: Path) -> np.ndarray:
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        with Image.open(image_path) as image:
            return np.array(image.convert("RGB"))

    @staticmethod
    def _save_rgb_array(image_array: np.ndarray, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(image_array.astype(np.uint8)).save(output_path)

    @staticmethod
    def _validate_matching_extensions(first_path: Path, second_path: Path) -> None:
        if first_path.suffix.lower() != second_path.suffix.lower():
            raise ValueError(
                "Images must have the same file extension: "
                f"{first_path.suffix} != {second_path.suffix}."
            )
