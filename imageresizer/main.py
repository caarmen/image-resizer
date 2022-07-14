"""
Server that provides an endpoint to resize an image
"""
import logging

import uvicorn
from fastapi import FastAPI

from imageresizer import purge
from imageresizer.repository import models
from imageresizer.routers import resize
from imageresizer.settings import settings

logging.basicConfig(
    filename=settings.get_log_absolute_path("image-resizer.log"), level=logging.INFO
)
logging.info("Started with settings %s", settings)

app = FastAPI(
    title="Image resizer",
    description="Api to reisze an image",
)

app.include_router(resize.router)


def setup():
    """
    Prepare for the app to run
    """
    models.create_db()
    purge.schedule()


if __name__ == "__main__":
    setup()
    uvicorn.run(
        "imageresizer.main:app",
        host="0.0.0.0",
        port=8000,
    )
