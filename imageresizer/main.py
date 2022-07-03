"""
Server that provides an endpoint to resize an image
"""
import os
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import uvicorn
from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from fastapi import BackgroundTasks, FastAPI
from fastapi.params import Query
from fastapi.responses import FileResponse

app = FastAPI(
    title="Image resizer",
    description="Api to reisze an image",
)


class GifImage:
    """
    An image-like class with resize and save functions
    """

    def __init__(self, source: GifImageFile):
        self._source = source
        self._frames = []

    def resize(self, size: tuple[int, int]):
        """
        Resize the frames of this image
        :param size: The requested size in pixels, as a 2-tuple:
           (width, height).
        :return: this instance
        """
        for i in range(self._source.n_frames):
            self._source.seek(i)
            self._frames.append(self._source.resize(size, resample=Image.BICUBIC))
        return self

    def save(self, output_path: str, image_format: str):
        """
        Saves this image under the given filename and format.
        """
        self._frames[0].save(
            output_path, append_images=self._frames[1:], format=image_format, save_all=True
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

    :param background_tasks: provided by Fast API
    :param image_url: the url of the image to resize
    :param width: the width of the new image
    :param height: the height of the new image
    :return: a Response containing the new image
    """
    with Image.open(urlopen(image_url)) as image:
        with NamedTemporaryFile(delete=False) as output_file:
            resized_width = width if width else image.width
            resized_height = height if height else image.height
            image_format = image.format

            if isinstance(image, GifImageFile) and image.n_frames:
                image = GifImage(image)

            image = image.resize((resized_width, resized_height))
            image.save(output_file.name, image_format)

            background_tasks.add_task(os.unlink, output_file.name)

            return FileResponse(output_file.name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)
