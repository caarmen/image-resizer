import os
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import uvicorn
from PIL import Image
from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/resize")
async def resize(image_url: str, background_tasks: BackgroundTasks):
    image = Image.open(urlopen(image_url))
    with NamedTemporaryFile(delete=False) as output_file:
        image.save(output_file.name, format=image.format)
        background_tasks.add_task(os.unlink, output_file.name)
        return FileResponse(output_file.name)
        # TODO replace temp file with cache


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)
