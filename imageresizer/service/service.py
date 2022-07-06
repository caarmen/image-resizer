"""
Image resizing service
"""
from os.path import exists
from tempfile import NamedTemporaryFile
from typing import Optional
from urllib.request import urlopen

from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from sqlalchemy.orm import Session

from imageresizer.repository import crud
from imageresizer.service import mapping
from imageresizer.service.animatedimage import AnimatedImage
from imageresizer.service.types import (
    Size,
    ImageFormat,
    ImageResponseData,
    ResizedImageLookup,
    ScaleType,
)
from imageresizer.settings import settings


def _is_valid_dimension(dimension):
    return dimension is not None and dimension > 0


def get_resized_size(
    source_size: Size,
    request_width: Optional[int],
    request_height: Optional[int],
    scale_type: ScaleType,
) -> Size:
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
    # No dimensions requested: return the original size
    if not valid_width and not valid_height:
        return source_size

    # Only one dimension requested: calculate the other one from
    # the original aspect ratio and the one dimension which is provided
    source_aspect_ratio = source_size[0] / source_size[1]
    if valid_width and not valid_height:
        return request_width, int(request_width / source_aspect_ratio)
    if not valid_width and valid_height:
        return int(request_height * source_aspect_ratio), request_height

    # Both dimensions provided

    if scale_type == ScaleType.FIT_XY:
        return request_width, request_height

    # Else fit the image inside the bounds of the requested dimensions,
    # preserving the original aspect ratio
    dest_aspect_ratio = request_width / request_height
    if source_aspect_ratio > dest_aspect_ratio:
        return request_width, int(request_width / source_aspect_ratio)
    return int(request_height * source_aspect_ratio), request_height


def _get_mime_type(image_format: ImageFormat) -> str:
    """
    :return: the mime type for the given image format
    """
    if image_format == ImageFormat.PDF:
        return "application/pdf"
    return f"image/{image_format}"


def resize(session: Session, lookup: ResizedImageLookup) -> ImageResponseData:
    """
    Resize an image.

    :param session: the database session
    :param lookup: the lookup fields for the image
    :return: the ImageResponse data for the resized image
    """

    crud_lookup = mapping.map_lookup(lookup)
    db_resized_image = crud.get_resized_image(session, crud_lookup)
    if db_resized_image and exists(db_resized_image.file):
        return ImageResponseData(
            db_resized_image.file, _get_mime_type(db_resized_image.image_format)
        )
    with Image.open(urlopen(lookup.url)) as image:
        with NamedTemporaryFile(
            delete=False, dir=settings.cache_image_dir
        ) as output_file:
            resized_size = get_resized_size(
                source_size=image.size,
                request_width=lookup.width,
                request_height=lookup.height,
                scale_type=lookup.scale_type,
            )
            resized_image_format = (
                lookup.image_format.name if lookup.image_format else image.format
            )

            if isinstance(image, GifImageFile) and image.n_frames:
                image = AnimatedImage(image)

            image = image.resize(resized_size)
            image.save(output_file.name, resized_image_format)
            if db_resized_image:
                crud.update_resized_image(
                    session, db_resized_image, file=output_file.name
                )
            else:
                crud.create_resized_image(session, crud_lookup, file=output_file.name)

            return ImageResponseData(
                file=output_file.name, mime_type=_get_mime_type(resized_image_format)
            )
