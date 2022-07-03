import os
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import uvicorn
from PIL import Image
from fastapi import BackgroundTasks, FastAPI
from fastapi.params import Query
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/resize")
async def resize(background_tasks: BackgroundTasks,
                 image_url: str,
                 width: int | None = Query(default=None, gt=0, lt=1024),
                 height: int | None = Query(default=None, gt=0, lt=1024)):
    image = Image.open(urlopen(image_url))
    with NamedTemporaryFile(delete=False) as output_file:
        resized_width = width if width else image.width
        resized_height = height if height else image.height
        image_format = image.format
        image = image.resize((resized_width, resized_height))
        image.save(output_file.name, format=image_format)
        background_tasks.add_task(os.unlink, output_file.name)
        return FileResponse(output_file.name)
        # TODO replace temp file with cache


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)
