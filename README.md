# Image resizer

An endpoint, using Fast API, that allows resizing an image.

[<img src="https://img.shields.io/badge/license-MIT-lightgrey.svg?maxAge=2592000">](https://github.com/caarmen/image-resizer/blob/main/LICENSE.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Usage:

Run the server:

### Locally
```commandline
pip install -r requirements/prod.txt
uvicorn imageresizer.main:app
```

### Using docker
```commandline
docker build -t imageresizer .
docker run --detach --publish 8000:8000 imageresizer
```

Browse the api docs at http://127.0.0.1:8000/docs

Use the `resize` endpoint.

Example resizing the [GitHub logo](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png) to 50x100:

http://127.0.0.1:8000/resize?image_url=https%3A%2F%2Fgithub.githubassets.com%2Fimages%2Fmodules%2Flogos_page%2FGitHub-Mark.png&width=50&height=100


## Generated API documentation
You can browse the documentation at the following links:

* Running on the server:
  - Redoc: http://localhost:8000/redoc
  - Swagger: http://localhost:8000/docs
  - Open api doc: http://localhost:8000/openapi.json
* Static documentation:
  - Github pages: https://caarmen.github.io/image-resizer/
