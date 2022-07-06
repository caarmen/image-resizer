"""
Image resizer tests
"""
from typing import Optional

from imageresizer.service.service import get_resized_size, Size


def _test_get_resized_size(
    source_size: Size,
    input_width: Optional[int],
    input_height: Optional[int],
    expected_output_size: Size,
):
    actual_output_size = get_resized_size(
        source_size=source_size,
        request_width=input_width,
        request_height=input_height,
    )
    assert expected_output_size == actual_output_size


def test_get_resized_size_no_input():
    """
    When no width or height are provided, return the source size
    """
    _test_get_resized_size((150, 100), None, None, (150, 100))


def test_get_resized_size_valid_width_and_height():
    """
    When a valid width and height are provided, return the provided width and height
    """
    _test_get_resized_size((150, 100), 25, 75, (25, 75))


def test_get_resized_size_zero_width_and_height():
    """
    When both width and height are zero, return the source size
    """
    _test_get_resized_size((150, 100), 0, 0, (150, 100))


def test_get_resized_size_negative_width_and_height():
    """
    When both width and height are negative, return the source size
    """
    _test_get_resized_size((150, 100), -1, -1, (150, 100))
    _test_get_resized_size((150, 100), -5, -5, (150, 100))


def test_get_missing_width():
    """
    When the width is missing, return the provided height with the width calculated
    from the aspect ratio of the source and the provided height
    """
    _test_get_resized_size((150, 100), None, 50, (75, 50))


def test_get_zero_width():
    """
    When the width is zero, return the provided height with the width calculated
    from the aspect ratio of the source and the provided height
    """
    _test_get_resized_size((150, 100), 0, 50, (75, 50))


def test_get_negative_width():
    """
    When the width is negative, return the provided height with the width calculated
    from the aspect ratio of the source and the provided height
    """
    _test_get_resized_size((150, 100), -1, 50, (75, 50))
    _test_get_resized_size((150, 100), -5, 50, (75, 50))


def test_get_missing_height():
    """
    When the height is missing, return the provided width with the height calculated
    from the aspect ratio of the source and the provided width
    """
    _test_get_resized_size((150, 100), 75, None, (75, 50))


def test_get_zero_height():
    """
    When the height is zero, return the provided width with the height calculated
    from the aspect ratio of the source and the provided width
    """
    _test_get_resized_size((150, 100), 75, 0, (75, 50))


def test_get_negative_height():
    """
    When the height is negative, return the provided width with the height calculated
    from the aspect ratio of the source and the provided width
    """
    _test_get_resized_size((150, 100), 75, -1, (75, 50))
    _test_get_resized_size((150, 100), 75, -5, (75, 50))
