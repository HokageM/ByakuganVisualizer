"""Image filter functions used by ByakuganVisualizer."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

RGBImageArray = np.ndarray
FilterFunction = Callable[[RGBImageArray], RGBImageArray]


def _ensure_rgb_image(image_data: RGBImageArray) -> None:
    """Validate that the input looks like an RGB image array."""
    if image_data.ndim != 3 or image_data.shape[2] < 3:
        raise ValueError(
            "Expected an RGB image array with shape (height, width, channels)."
        )


def keep_channels(
    image_data: RGBImageArray, channels: tuple[int, ...]
) -> RGBImageArray:
    """Return a copy of the image where only the selected RGB channels remain."""
    _ensure_rgb_image(image_data)

    filtered = np.zeros_like(image_data)
    for channel in channels:
        filtered[:, :, channel] = image_data[:, :, channel]
    return filtered


def keep_red(image_data: RGBImageArray) -> RGBImageArray:
    """Keep only the red channel."""
    return keep_channels(image_data, (0,))


def keep_green(image_data: RGBImageArray) -> RGBImageArray:
    """Keep only the green channel."""
    return keep_channels(image_data, (1,))


def keep_blue(image_data: RGBImageArray) -> RGBImageArray:
    """Keep only the blue channel."""
    return keep_channels(image_data, (2,))


def keep_yellow(image_data: RGBImageArray) -> RGBImageArray:
    """Keep the red and green channels, producing a yellow-like filter."""
    return keep_channels(image_data, (0, 1))


def correction_for_colorblindness(
    image_array: RGBImageArray,
    degree_protanomaly: float,
    degree_deuteranomaly: float,
) -> RGBImageArray:
    """Apply a simple protanomaly/deuteranomaly correction matrix.

    The input image is converted to float during calculation to avoid uint8
    overflow/underflow. The result is clipped back into the valid RGB range.
    """
    _ensure_rgb_image(image_array)

    if degree_protanomaly < 0 or degree_deuteranomaly < 0:
        raise ValueError("Colorblindness correction degrees must be >= 0.")

    r = image_array[..., 0].astype(float)
    g = image_array[..., 1].astype(float)
    b = image_array[..., 2].astype(float)

    corrected = image_array.astype(float).copy()

    corrected[..., 0] = (1 - degree_deuteranomaly / 2) * r + (
        degree_deuteranomaly / 2
    ) * g
    corrected[..., 1] = (degree_protanomaly / 2) * r + (1 - degree_protanomaly / 2) * g
    corrected[..., 2] = (
        (degree_protanomaly / 4) * r
        + (degree_deuteranomaly / 4) * g
        + (1 - (degree_deuteranomaly + degree_protanomaly) / 4) * b
    )

    return np.clip(corrected, 0, 255).astype(np.uint8)


FILTERS: dict[str, FilterFunction] = {
    "red": keep_red,
    "green": keep_green,
    "blue": keep_blue,
    "yellow": keep_yellow,
}
