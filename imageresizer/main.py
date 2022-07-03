"""
Server that provides an endpoint to resize an image
"""
import os

import uvicorn
from fastapi import BackgroundTasks, FastAPI
from fastapi.params import Query
from fastapi.responses import FileResponse

from imageresizer import service

app = FastAPI(
    title="Image resizer",
    description="Api to reisze an image",
)


@app.get("/resize")
async def resize(
    background_tasks: BackgroundTasks,
    image_url: str,
    width: int | None = Query(default=None, gt=0, lt=1024),
    height: int | None = Query(default=None, gt=0, lt=1024),
):
    """
    Endpoint to resize an image.

    :param image_url: the url of the image to resize
    :param width: the width of the new image
    :param height: the height of the new image
    :return: a Response containing the new image
    """
    resized_image_path = service.resize(image_url, width, height)
    background_tasks.add_task(os.unlink, resized_image_path)
    return FileResponse(resized_image_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
