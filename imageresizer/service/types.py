"""
Image resizing service types
"""
import dataclasses
from enum import Enum

Size = tuple[int, int]


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


@dataclasses.dataclass
class ResizedImageLookup:
    """
    Fields which uniquely identify a resised image in the database
    """

    url: str
    width: int = 0
    height: int = 0
    image_format: ImageFormat = None
