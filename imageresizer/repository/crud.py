"""
Provide CRUD operations for resized images
"""
from datetime import datetime

from sqlalchemy.orm import Session

from imageresizer.repository import models


def get_resized_image(session: Session, url: str, width: int, height: int):
    """
    Read the resized image with the matching url, width and height,  from the database, if it exists
    """
    return (
        session.query(models.ResizedImage)
        .filter(
            models.ResizedImage.url == url,
            models.ResizedImage.width == width,
            models.ResizedImage.height == height,
        )
        .first()
    )


def create_resized_image(
    session: Session, url: str, width: int, height: int, file: str
):
    """
    Create the resized image in the database
    """
    db_resized_image = models.ResizedImage(
        url=url, width=width, height=height, file=file, datetime=datetime.now()
    )
    session.add(db_resized_image)
    session.commit()
    session.refresh(db_resized_image)
    return db_resized_image


def update_resized_image(
    session: Session, db_resized_image: models.ResizedImage, file: str
):
    """
    Create the resized image's file and timestamp in the database
    """
    db_resized_image.file = file
    db_resized_image.datetime = datetime.now()
    session.commit()
    session.refresh(db_resized_image)
    return db_resized_image
