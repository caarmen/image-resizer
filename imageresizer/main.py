"""
Server that provides an endpoint to resize an image
"""
import logging
from urllib.error import HTTPError

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Query, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.requests import Request

from imageresizer import purge
from imageresizer.repository import models
from imageresizer.repository.database import SessionLocal, engine
from imageresizer.service import service
from imageresizer.service.types import ImageFormat, ResizedImageLookup, ScaleType
from imageresizer.settings import settings

logging.basicConfig(filename="image-resizer.log", level=logging.INFO)
logging.info("Started with settings %s", settings)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Image resizer",
    description="Api to reisze an image",
)


def _get_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


with SessionLocal() as session:
    purge.purge_old_images(session)


# pylint: disable=too-many-arguments
@app.get("/resize")
async def resize(
    request: Request,
    image_url: str,
    width: int | None = Query(default=None, gt=0, lt=1024),
    height: int | None = Query(default=None, gt=0, lt=1024),
    image_format: ImageFormat | None = Query(default=None),
    scale_type: ScaleType | None = Query(default=ScaleType.FIT_XY),
    db_session: Session = Depends(_get_session),
):
    """
    Endpoint to resize an image.

    :param image_url: the url of the image to resize

    :param width: the width of the new image

    :param height: the height of the new image

    :param image_format: the format of the resized image. Defaults to the format of the source image

    :param scale_type: controls how the image should be resized to match
    the requested width and height

    :return: a Response containing the new image
    """
    if request.headers.get("x-image-resizer"):
        raise HTTPException(status_code=400, detail="Invalid image url")
    try:
        resized_image = service.resize(
            db_session,
            headers={
                "x-image-resizer": "true",
            },
            lookup=ResizedImageLookup(
                url=image_url,
                width=width,
                height=height,
                image_format=image_format,
                scale_type=scale_type,
            ),
        )
        return FileResponse(resized_image.file, media_type=resized_image.mime_type)
    except HTTPError as error:
        raise HTTPException(status_code=error.status, detail=error.reason) from error


if __name__ == "__main__":
    uvicorn.run(
        "imageresizer.main:app",
        host="0.0.0.0",
        port=8000,
        workers=settings.worker_count,
        reload=False,
    )
