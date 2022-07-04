"""
ORM model for the image-resizer database
"""
from sqlalchemy import Column, Integer, String, Index, DateTime

from imageresizer.repository.database import Base


# pylint: disable=too-few-public-methods
class ResizedImage(Base):
    """
    Model for a resized image
    """

    __tablename__ = "resized_images"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    file = Column(String)
    image_format = Column(String)
    datetime = Column(DateTime)


Index(
    "resize-image-index",
    ResizedImage.url,
    ResizedImage.width,
    ResizedImage.height,
    ResizedImage.image_format,
    unique=True,
)
