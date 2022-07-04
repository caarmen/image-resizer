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
