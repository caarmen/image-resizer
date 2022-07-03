"""
Image resizer tests
"""
from typing import Optional

from imageresizer.service import get_resized_size, Size


def _test_get_resized_size(
    source_size: Size,
    input_width: Optional[int],
    input_height: Optional[int],
    expected_output_size: Size,
):
    actual_output_size = get_resized_size(source_size=source_size, request_width=input_width,
                                          request_height=input_height)
    assert expected_output_size == actual_output_size


def test_get_resized_size_no_input():
    _test_get_resized_size((150, 100), None, None, (150, 100))


def test_get_resized_size_valid_width_and_height():
    _test_get_resized_size((150, 100), 25, 75, (25, 75))


def test_get_resized_size_zero_width_and_height():
    _test_get_resized_size((150, 100), 0, 0, (150, 100))


def test_get_resized_size_negative_width_and_height():
    _test_get_resized_size((150, 100), -1, -1, (150, 100))
    _test_get_resized_size((150, 100), -5, -5, (150, 100))


def test_get_missing_width():
    _test_get_resized_size((150, 100), None, 50, (75, 50))


def test_get_zero_width():
    _test_get_resized_size((150, 100), 0, 50, (75, 50))


def test_get_negative_width():
    _test_get_resized_size((150, 100), -1, 50, (75, 50))
    _test_get_resized_size((150, 100), -5, 50, (75, 50))


def test_get_missing_height():
    _test_get_resized_size((150, 100), 75, None, (75, 50))


def test_get_zero_height():
    _test_get_resized_size((150, 100), 75, 0, (75, 50))


def test_get_negative_height():
    _test_get_resized_size((150, 100), 75, -1, (75, 50))
    _test_get_resized_size((150, 100), 75, -5, (75, 50))
