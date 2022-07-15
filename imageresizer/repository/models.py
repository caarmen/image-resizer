"""
ORM model for the image-resizer database
"""

from sqlalchemy import Column, Integer, String, Index, DateTime

from imageresizer.repository.database import Base, engine

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
    # Would be better to have an enum for vaild image_format values
    image_format = Column(Integer)
    scale_type = Column(Integer)
    file = Column(String)
    mime_type = Column(String)
    datetime = Column(DateTime)


Index(
    "resize-image-index",
    ResizedImage.url,
    ResizedImage.width,
    ResizedImage.height,
    ResizedImage.image_format,
    ResizedImage.scale_type,
    unique=True,
)


def create_db():
    """
    Creates the database if it doesn't already exist
    """
    Base.metadata.create_all(bind=engine, checkfirst=True)
