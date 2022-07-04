"""
Utility to delete old resized images
"""
import argparse
import datetime
import logging
import os
from os.path import exists

from sqlalchemy.orm import Session

from imageresizer.repository import models
from imageresizer.repository.database import SessionLocal, engine

DEFAULT_MAX_AGE_S = 86400


def purge_old_images(session: Session, max_age_seconds: int = DEFAULT_MAX_AGE_S):
    """
    Delete resized image data from the db and the disk,
    for resized images created or updated before max_age_seconds ago
    """
    datetime_limit = datetime.datetime.now() - datetime.timedelta(
        seconds=max_age_seconds
    )
    logging.info("Deleting images created before %s", datetime_limit)
    resized_images_to_delete = session.query(models.ResizedImage).filter(
        models.ResizedImage.datetime <= datetime_limit
    )
    logging.info("Found %s images", resized_images_to_delete.count())
    for resized_image in resized_images_to_delete:
        # pylint: disable=line-too-long
        file_log = f"{resized_image.url}({resized_image.width}x{resized_image.height}): {resized_image.file}"
        if exists(resized_image.file):
            os.unlink(resized_image.file)
            logging.debug("Deleted %s", file_log)
        else:
            logging.debug("File %s was already deleted", file_log)

    resized_images_to_delete.delete()
    session.commit()


if __name__ == "__main__":
    logging.basicConfig(filename="purge.log", level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="Purge old images")
    parser.add_argument(
        "--max-age",
        dest="max_age",
        type=int,
        default=DEFAULT_MAX_AGE_S,
        help="max age in seconds to keep in the database. Default is %(default)s",
    )
    options = parser.parse_args()
    models.Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        purge_old_images(db, options.max_age)