"""
Image resizing service types
"""
import dataclasses
from enum import Enum


@dataclasses.dataclass
class ImageResponseData:
    """
    Image response data
    """

    file: str
    mime_type: str


class ImageFormat(str, Enum):
    """
    Supported image formats
    """

    BMP = "bmp"
    GIF = "gif"
    JPEG = "jpeg"
    PDF = "pdf"
    PNG = "png"
    TIFF = "tiff"
    WEBP = "webp"


class ScaleType(str, Enum):
    """
    Supported scale types
    """

    FIT_XY = "fit_xy"
    FIT_PRESERVE_ASPECT_RATIO = "fit_preserve_aspect_ratio"
    CROP = "crop"


@dataclasses.dataclass
# pylint: disable=duplicate-code
class ResizedImageLookup:
    """
    Fields which uniquely identify a resised image in the database
    """

    url: str
    width: int = 0
    height: int = 0
    image_format: ImageFormat = None
    scale_type: ScaleType = ScaleType.FIT_XY
