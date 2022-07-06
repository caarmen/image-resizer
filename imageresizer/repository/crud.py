"""
Provide CRUD operations for resized images
"""
import dataclasses
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Session

from imageresizer.repository import models


class ScaleType(Enum):
    """
    Supported scaling types
    """

    FIT_XY = 1
    FIT_PRESERVE_ASPECT_RATIO = 2


@dataclasses.dataclass
class ResizedImageLookup:
    """
    Fields which uniquely identify a resised image in the database
    """

    url: str
    width: int = 0
    height: int = 0
    image_format: str = None
    scale_type: ScaleType = None


def get_resized_image(
    session: Session, lookup: ResizedImageLookup
) -> models.ResizedImage:
    """
    Read the resized image with the matching url, width, height, and image format,
    from the database, if it exists
    """
    return (
        session.query(models.ResizedImage)
        .filter(
            models.ResizedImage.url == lookup.url,
            models.ResizedImage.width == lookup.width,
            models.ResizedImage.height == lookup.height,
            models.ResizedImage.image_format == lookup.image_format,
            models.ResizedImage.scale_type == lookup.scale_type.value,
        )
        .first()
    )


def create_resized_image(
    session: Session,
    lookup: ResizedImageLookup,
    file: str,
    mime_type: str,
) -> models.ResizedImage:
    """
    Create the resized image in the database
    """
    db_resized_image = models.ResizedImage(
        url=lookup.url,
        width=lookup.width,
        height=lookup.height,
        image_format=lookup.image_format,
        scale_type=lookup.scale_type.value,
        file=file,
        mime_type=mime_type,
        datetime=datetime.now(),
    )
    session.add(db_resized_image)
    session.commit()
    session.refresh(db_resized_image)
    return db_resized_image


def update_resized_image(
    session: Session, db_resized_image: models.ResizedImage, file: str
) -> models.ResizedImage:
    """
    Create the resized image's file and timestamp in the database
    """
    db_resized_image.file = file
    db_resized_image.datetime = datetime.now()
    session.commit()
    session.refresh(db_resized_image)
    return db_resized_image
