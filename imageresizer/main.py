"""
Server that provides an endpoint to resize an image
"""
import logging

import uvicorn
from fastapi import FastAPI

from imageresizer import purge
from imageresizer.repository import models
from imageresizer.repository.database import SessionLocal, engine
from imageresizer.routers import resize
from imageresizer.settings import settings

logging.basicConfig(filename="image-resizer.log", level=logging.INFO)
logging.info("Started with settings %s", settings)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Image resizer",
    description="Api to reisze an image",
)

with SessionLocal() as session:
    purge.purge_old_images(session)

app.include_router(resize.router)

if __name__ == "__main__":
    uvicorn.run(
        "imageresizer.main:app",
        host="0.0.0.0",
        port=8000,
        workers=settings.worker_count,
        reload=False,
    )
