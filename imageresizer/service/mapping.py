"""
Image resizing service types
"""

from imageresizer.repository import crud
from imageresizer.service.types import ScaleType, ResizedImageLookup, ImageFormat

Size = tuple[int, int]


def _map_image_format(service_image_format: ImageFormat) -> crud.ImageFormat | None:
    """
    Convert a service ImageFormat to a repository ImageFormat
    """
    # I understand avoiding too many return statements if it can make the flow
    # difficult to follow. In this case I don't think it's the case, so I
    # ignore this lint rule here
    # pylint: disable=too-many-return-statements
    match service_image_format:
        case ImageFormat.BMP:
            return crud.ImageFormat.BMP
        case ImageFormat.GIF:
            return crud.ImageFormat.GIF
        case ImageFormat.JPEG:
            return crud.ImageFormat.JPEG
        case ImageFormat.PDF:
            return crud.ImageFormat.PDF
        case ImageFormat.PNG:
            return crud.ImageFormat.PNG
        case ImageFormat.TIFF:
            return crud.ImageFormat.TIFF
        case ImageFormat.WEBP:
            return crud.ImageFormat.WEBP
        case _:
            return None


def _map_scale_type(service_scale_type: ScaleType) -> crud.ScaleType:
    """
    Convert a service ScaleType to a repository ScaleType
    """
    if service_scale_type == ScaleType.FIT_XY:
        return crud.ScaleType.FIT_XY
    return crud.ScaleType.FIT_PRESERVE_ASPECT_RATIO


def map_lookup(service_lookup: ResizedImageLookup) -> crud.ResizedImageLookup:
    """
    Convert a service lookup to a repository lookup
    """
    return crud.ResizedImageLookup(
        url=service_lookup.url,
        width=service_lookup.width,
        height=service_lookup.height,
        image_format=_map_image_format(service_lookup.image_format),
        scale_type=_map_scale_type(service_lookup.scale_type),
    )
