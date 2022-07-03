import os
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import uvicorn
from PIL import Image
from fastapi import BackgroundTasks, FastAPI
from fastapi.params import Query
from fastapi.responses import FileResponse

app = FastAPI()


def _resize_save_image_sequence(
        image: Image,
        width: int,
        height: int,
        output_path: str) -> Image:
    frames = []
    for i in range(image.n_frames):
        image.seek(i)
        frames.append(image.resize((width, height), resample=Image.BICUBIC))
    frames[0].save(output_path, append_images=frames[1:], format=image.format, save_all=True)


def _resize_save_image(
        image: Image,
        width: int,
        height: int,
        output_path: str) -> Image:
    image_format = image.format
    image = image.resize((width, height))
    image.save(output_path, format=image_format)


@app.get("/resize")
async def resize(
        background_tasks: BackgroundTasks,
        image_url: str,
        width: int | None = Query(default=None, gt=0, lt=1024),
        height: int | None = Query(default=None, gt=0, lt=1024)):
    image = Image.open(urlopen(image_url))
    with NamedTemporaryFile(delete=False) as output_file:
        resized_width = width if width else image.width
        resized_height = height if height else image.height
        if hasattr(image, "n_frames") and image.n_frames:
            _resize_save_image_sequence(image, resized_width, resized_height, output_file.name)
        else:
            _resize_save_image(image, resized_width, resized_height, output_file.name)
        background_tasks.add_task(os.unlink, output_file.name)
        return FileResponse(output_file.name)
        # TODO replace temp file with cache


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)
