"""
Image resizer tests
"""
from typing import Optional

import pytest

from imageresizer.service.geometry import ResizeGeometry, get_resize_geometry, Size, Box
from imageresizer.service.types import ScaleType


def _test_get_resize_geometry(
    source_size: Size,
    input_width: Optional[int],
    input_height: Optional[int],
    input_scale_type: ScaleType,
    expected_output_resize_geometry: ResizeGeometry,
):
    actual_output_resize_geometry = get_resize_geometry(
        source_size=source_size,
        request_width=input_width,
        request_height=input_height,
        scale_type=input_scale_type,
    )
    assert actual_output_resize_geometry == expected_output_resize_geometry


@pytest.mark.parametrize("scale_type", ScaleType)
def test_get_resize_geometry_no_input(scale_type: ScaleType):
    """
    When no width or height are provided, return the source size
    """
    _test_get_resize_geometry(
        (150, 100), None, None, scale_type, ResizeGeometry(size=(150, 100))
    )


def test_get_resize_geometry_valid_width_and_height_fit_xy():
    """
    When a valid width and height are provided with fit_xy scale type,
    return the provided width and height
    """
    _test_get_resize_geometry(
        (150, 100), 25, 75, ScaleType.FIT_XY, ResizeGeometry(size=(25, 75))
    )


def test_get_resize_geometry_valid_width_and_height_fit_preserve_aspect_ratio():
    """
    When a valid width and height are provided with fit_preserve_aspect_ratio scale type,
    return the expected width and height
    """
    _test_get_resize_geometry(
        (150, 100),
        25,
        75,
        ScaleType.FIT_PRESERVE_ASPECT_RATIO,
        ResizeGeometry(size=(25, 16)),
    )
    _test_get_resize_geometry(
        (150, 100),
        750,
        25,
        ScaleType.FIT_PRESERVE_ASPECT_RATIO,
        ResizeGeometry(size=(37, 25)),
    )


def test_get_resize_geometry_valid_width_and_height_crop():
    """
    When a valid width and height are provided with crop scale_type,
    return the expected width and height
    """
    _test_get_resize_geometry(
        (150, 100),
        25,
        75,
        ScaleType.CROP,
        ResizeGeometry(size=(25, 75), box=Box(left=58, top=0, right=91, bottom=100)),
    )
    _test_get_resize_geometry(
        (150, 100),
        750,
        25,
        ScaleType.CROP,
        ResizeGeometry(size=(750, 25), box=Box(left=0, top=47, right=150, bottom=52)),
    )
    _test_get_resize_geometry(
        (560, 560),
        50,
        100,
        ScaleType.CROP,
        ResizeGeometry(size=(50, 100), box=Box(left=140, top=0, right=420, bottom=560)),
    )


@pytest.mark.parametrize("scale_type", ScaleType)
def test_get_resize_geometry_zero_width_and_height(scale_type: ScaleType):
    """
    When both width and height are zero, return the source size
    """
    _test_get_resize_geometry(
        (150, 100), 0, 0, scale_type, ResizeGeometry(size=(150, 100))
    )


@pytest.mark.parametrize("scale_type", ScaleType)
def test_get_resize_geometry_negative_width_and_height(scale_type: ScaleType):
    """
    When both width and height are negative, return the source size
    """
    _test_get_resize_geometry(
        (150, 100), -1, -1, scale_type, ResizeGeometry(size=(150, 100))
    )
    _test_get_resize_geometry(
        (150, 100), -5, -5, scale_type, ResizeGeometry(size=(150, 100))
    )


@pytest.mark.parametrize("scale_type", ScaleType)
def test_get_missing_width(scale_type: ScaleType):
    """
    When the width is missing, return the provided height with the width calculated
    from the aspect ratio of the source and the provided height
    """
    _test_get_resize_geometry(
        (150, 100), None, 50, scale_type, ResizeGeometry(size=(75, 50))
    )


@pytest.mark.parametrize("scale_type", ScaleType)
def test_get_zero_width(scale_type: ScaleType):
    """
    When the width is zero, return the provided height with the width calculated
    from the aspect ratio of the source and the provided height
    """
    _test_get_resize_geometry(
        (150, 100), 0, 50, scale_type, ResizeGeometry(size=(75, 50))
    )


@pytest.mark.parametrize("scale_type", ScaleType)
def test_get_negative_width(scale_type: ScaleType):
    """
    When the width is negative, return the provided height with the width calculated
    from the aspect ratio of the source and the provided height
    """
    _test_get_resize_geometry(
        (150, 100), -1, 50, scale_type, ResizeGeometry(size=(75, 50))
    )
    _test_get_resize_geometry(
        (150, 100), -5, 50, scale_type, ResizeGeometry(size=(75, 50))
    )


@pytest.mark.parametrize("scale_type", ScaleType)
def test_get_missing_height(scale_type: ScaleType):
    """
    When the height is missing, return the provided width with the height calculated
    from the aspect ratio of the source and the provided width
    """
    _test_get_resize_geometry(
        (150, 100), 75, None, scale_type, ResizeGeometry(size=(75, 50))
    )


@pytest.mark.parametrize("scale_type", ScaleType)
def test_get_zero_height(scale_type: ScaleType):
    """
    When the height is zero, return the provided width with the height calculated
    from the aspect ratio of the source and the provided width
    """
    _test_get_resize_geometry(
        (150, 100), 75, 0, scale_type, ResizeGeometry(size=(75, 50))
    )


@pytest.mark.parametrize("scale_type", ScaleType)
def test_get_negative_height(scale_type: ScaleType):
    """
    When the height is negative, return the provided width with the height calculated
    from the aspect ratio of the source and the provided width
    """
    _test_get_resize_geometry(
        (150, 100), 75, -1, scale_type, ResizeGeometry(size=(75, 50))
    )
    _test_get_resize_geometry(
        (150, 100), 75, -5, scale_type, ResizeGeometry(size=(75, 50))
    )
