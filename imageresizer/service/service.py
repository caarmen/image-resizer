"""
Image resizing service
"""
from os.path import exists
from tempfile import NamedTemporaryFile
from typing import Optional
from urllib.request import urlopen

from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from fastapi.params import Query
from sqlalchemy.orm import Session

from imageresizer.repository import crud
from imageresizer.service.animatedimage import AnimatedImage
from imageresizer.service.types import Size, ImageFormat, ImageResponseData


def _is_valid_dimension(dimension):
    return dimension is not None and dimension > 0


def get_resized_size(
    source_size: Size,
    request_width: Optional[int],
    request_height: Optional[int],
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
    :return: the target size the image should be resized to
    """
    valid_width = _is_valid_dimension(request_width)
    valid_height = _is_valid_dimension(request_height)
    if valid_width and valid_height:
        return request_width, request_height
    if not valid_width and not valid_height:
        return source_size

    source_aspect_ratio = source_size[0] / source_size[1]

    if valid_width:
        return request_width, int(request_width / source_aspect_ratio)
    return int(request_height * source_aspect_ratio), request_height


def _get_mime_type(image_format: str) -> str:
    """
    :return: the mime type for the given image format
    """
    if image_format == ImageFormat.PDF.value:
        return "application/pdf"
    return f"image/{image_format}"


def resize(
    session: Session,
    image_url: str,
    width: int | None = Query(default=None, gt=0, lt=1024),
    height: int | None = Query(default=None, gt=0, lt=1024),
    image_format: ImageFormat | None = Query(default=None),
) -> ImageResponseData:
    """
    Resize an image.

    :param session: the database session
    :param image_url: the url of the image to resize
    :param width: the width of the new image
    :param height: the height of the new image
    :param image_format: the format of the resized image. Defaults to the format of the source image
    :return: the path to the file containing the resized image
    """
    db_resized_image = crud.get_resized_image(
        session, url=image_url, width=width, height=height, image_format=image_format
    )
    if db_resized_image and exists(db_resized_image.file):
        return ImageResponseData(
            db_resized_image.file, _get_mime_type(db_resized_image.image_format)
        )
    with Image.open(urlopen(image_url)) as image:
        with NamedTemporaryFile(delete=False) as output_file:
            resized_size = get_resized_size(
                source_size=image.size, request_width=width, request_height=height
            )
            resized_image_format = image_format.name if image_format else image.format

            if isinstance(image, GifImageFile) and image.n_frames:
                image = AnimatedImage(image)

            image = image.resize(resized_size)
            image.save(output_file.name, resized_image_format)
            if db_resized_image:
                crud.update_resized_image(
                    session, db_resized_image, file=output_file.name
                )
            else:
                crud.create_resized_image(
                    session,
                    url=image_url,
                    width=width,
                    height=height,
                    file=output_file.name,
                    image_format=image_format,
                )

            return ImageResponseData(
                file=output_file.name, mime_type=_get_mime_type(image_format)
            )
