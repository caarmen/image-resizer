from fastapi import FastAPI
import httpx
from fastapi.params import Query
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/resize")
async def resize(image_url: str = Query(None)):
    async with httpx.AsyncClient() as client:
        external_response = await client.get(image_url)
        with open("/tmp/foo", "wb") as file:
            file.write(external_response.content)
        return FileResponse("/tmp/foo")
