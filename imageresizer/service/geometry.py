"""
Geometric calculations for resizing images
"""
import dataclasses
from typing import Optional

from imageresizer.service.types import ScaleType

Size = tuple[int, int]


@dataclasses.dataclass
class Box:
    """
    Defines a zone inside an image
    """

    left: int
    top: int
    right: int
    bottom: int


@dataclasses.dataclass
class ResizeGeometry:
    """
    Determines how an image should be resized
    """

    size: Size
    box: Box = None


def _is_valid_dimension(dimension):
    return dimension is not None and dimension > 0


def _get_resize_geometry_partial_requested_size(
    source_size: Size,
    request_width: Optional[int],
    request_height: Optional[int],
) -> ResizeGeometry:
    # No dimensions requested: return the original size
    if not request_width and not request_height:
        return ResizeGeometry(size=source_size)

    # Only one dimension requested: calculate the other one from
    # the original aspect ratio and the one dimension which is provided
    source_aspect_ratio = source_size[0] / source_size[1]
    if request_width and not request_height:
        return ResizeGeometry(
            size=(request_width, int(request_width / source_aspect_ratio))
        )
    # not request_width and request_height:
    return ResizeGeometry(
        size=(int(request_height * source_aspect_ratio), request_height)
    )


def _get_resize_geometry_fit_xy(
    _: Size,
    request_width: Optional[int],
    request_height: Optional[int],
) -> ResizeGeometry:
    return ResizeGeometry(size=(request_width, request_height))


def _get_resize_geometry_crop(
    source_size: Size,
    request_width: Optional[int],
    request_height: Optional[int],
) -> ResizeGeometry:
    # Resize the image so that it fills the requested size, without distorting the image,
    # but cropping along one axis if the aspect ratio of the source is different from the
    # requested aspect ratio
    source_aspect_ratio = source_size[0] / source_size[1]
    dest_aspect_ratio = request_width / request_height
    if source_aspect_ratio > dest_aspect_ratio:
        return ResizeGeometry(
            size=(request_width, request_height),
            box=Box(
                left=int(
                    (source_size[0] - (request_width * source_size[1] / request_height))
                    / 2
                ),
                top=0,
                right=int(
                    (source_size[0] + (request_width * source_size[1] / request_height))
                    / 2
                ),
                bottom=source_size[1],
            ),
        )
    return ResizeGeometry(
        size=(request_width, request_height),
        box=Box(
            left=0,
            top=int(
                (source_size[1] - (request_height * source_size[0] / request_width)) / 2
            ),
            right=source_size[0],
            bottom=int(
                (source_size[1] + (request_height * source_size[0] / request_width)) / 2
            ),
        ),
    )


def _get_resize_geometry_fit_preserve_aspect_ratio(
    source_size: Size,
    request_width: Optional[int],
    request_height: Optional[int],
) -> ResizeGeometry:
    source_aspect_ratio = source_size[0] / source_size[1]
    # Else fit the image inside the bounds of the requested dimensions,
    # preserving the original aspect ratio
    dest_aspect_ratio = request_width / request_height
    if source_aspect_ratio > dest_aspect_ratio:
        return ResizeGeometry(
            size=(request_width, int(request_width / source_aspect_ratio))
        )
    return ResizeGeometry(
        size=(int(request_height * source_aspect_ratio), request_height)
    )


def get_resize_geometry(
    source_size: Size,
    request_width: Optional[int],
    request_height: Optional[int],
    scale_type: ScaleType,
) -> ResizeGeometry:
    """
    Calculate a new resized size based on a source size and optional new width and height.

    If neither the requested width nor height are positive integers, return the source size.

    If one of the requested width or requested height is not a positive integer, then return a
    target size whose corresponding width or height is calculated based on the aspect ratio of
    the source.

    :param source_size: the size of the source image
    :param request_width: the requested width of the target image
    :param request_height: the requested height of the target image
    :param scale_type: controls how the image should be resized to match the requested
    width and height
    :return: the target size the image should be resized to
    """
    valid_width = _is_valid_dimension(request_width)
    valid_height = _is_valid_dimension(request_height)
    if not valid_width or not valid_height:
        return _get_resize_geometry_partial_requested_size(
            source_size=source_size,
            request_width=request_width if valid_width else None,
            request_height=request_height if valid_height else None,
        )

    # Both dimensions provided
    match scale_type:
        case ScaleType.FIT_XY:
            return _get_resize_geometry_fit_xy(
                source_size, request_width, request_height
            )
        case ScaleType.CROP:
            return _get_resize_geometry_crop(source_size, request_width, request_height)
        case _:  # ScaleType.FIT_PRESERVE_ASPECT_RATIO:
            return _get_resize_geometry_fit_preserve_aspect_ratio(
                source_size, request_width, request_height
            )
