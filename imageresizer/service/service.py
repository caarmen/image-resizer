"""
Image resizing service
"""
import dataclasses
from os.path import exists
from tempfile import NamedTemporaryFile
from urllib.request import urlopen, Request

from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from sqlalchemy.orm import Session

from imageresizer.repository import crud
from imageresizer.service import mapping, geometry
from imageresizer.service.animatedimage import AnimatedImage
from imageresizer.service.types import (
    ImageFormat,
    ImageResponseData,
    ResizedImageLookup,
)
from imageresizer.settings import settings


def _get_mime_type(image_format: ImageFormat) -> str:
    """
    :return: the mime type for the given image format
    """
    if image_format == ImageFormat.PDF:
        return "application/pdf"
    return f"image/{image_format}"


def resize(
    session: Session, headers: dict[str, str], lookup: ResizedImageLookup
) -> ImageResponseData:
    """
    Resize an image.

    :param session: the database session
    :param headers: headers to use in the request to fetch time image
    :param lookup: the lookup fields for the image
    :return: the ImageResponse data for the resized image
    """

    crud_lookup = mapping.map_lookup(lookup)
    db_resized_image = crud.get_resized_image(session, crud_lookup)
    if db_resized_image and exists(db_resized_image.file):
        return ImageResponseData(db_resized_image.file, db_resized_image.mime_type)
    with Image.open(urlopen(Request(lookup.url, headers=headers))) as image:
        with NamedTemporaryFile(
            delete=False, dir=settings.cache_image_dir
        ) as output_file:
            resize_geometry = geometry.get_resize_geometry(
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

            image = image.resize(
                size=resize_geometry.size,
                box=dataclasses.astuple(resize_geometry.box)
                if resize_geometry.box
                else None,
            )
            image.save(output_file.name, resized_image_format)
            mime_type = _get_mime_type(resized_image_format)
            if db_resized_image:
                crud.update_resized_image(
                    session, db_resized_image, file=output_file.name
                )
            else:
                crud.create_resized_image(
                    session, crud_lookup, file=output_file.name, mime_type=mime_type
                )

            return ImageResponseData(file=output_file.name, mime_type=mime_type)
