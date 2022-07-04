"""
Server that provides an endpoint to resize an image
"""
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.params import Query, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from imageresizer import service, purge
from imageresizer.repository import models
from imageresizer.repository.database import SessionLocal, engine

logging.basicConfig(filename="image-resizer.log", level=logging.INFO)

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


@app.get("/resize")
async def resize(
    image_url: str,
    width: int | None = Query(default=None, gt=0, lt=1024),
    height: int | None = Query(default=None, gt=0, lt=1024),
    db_session: Session = Depends(_get_session),
):
    """
    Endpoint to resize an image.

    :param image_url: the url of the image to resize

    :param width: the width of the new image

    :param height: the height of the new image

    :return: a Response containing the new image
    """
    resized_image_path = service.resize(db_session, image_url, width, height)
    return FileResponse(resized_image_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
