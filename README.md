# Image resizer

An endpoint, using Fast API, that allows resizing an image.

[<img src="https://img.shields.io/badge/license-MIT-lightgrey.svg?maxAge=2592000">](https://github.com/caarmen/image-resizer/blob/main/LICENSE.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[<img src="https://github.com/caarmen/image-resizer/actions/workflows/tests.yml/badge.svg">](https://github.com/caarmen/image-resizer/actions?query=workflow%3A%22Run+tests%22++)

## Run the server

### Locally

```bash
pip install -r requirements/prod.txt
uvicorn imageresizer.main:app
```

### Using docker

```bash
git clone https://github.com/caarmen/image-resizer.git
cd image-resizer
docker build -t imageresizer .
docker run --detach --publish 8000:8000 imageresizer
```

#### Custom port

If you want the server to be available on a port other than `8000`,
you can specify the port you want in the `--publish` argument.

For example, to use port `8102` instead:

```bash
docker run --detach --publish 8102:8000 imageresizer
```

#### Custom cache folder

If you want to store the image resizer cache on the host machine,
you can specify this with the `--volume` argument, mapping the host folder you want (ex: `/tmp/foo`)
to the folder inside the docker image where the image cache is stored (`/var/cache/image-resizer`):

```bash
docker run --detach --volume /tmp/foo:/var/cache/image-resizer --publish 8000:8000 imageresizer
```

#### Worker count

By default, the server runs with one worker. To change this, specify the number of workers with the
`WEB_CONCURRENCY` environment variable. For example, to set 4 workers:

```bash
docker run --detach --env WEB_CONCURRENCY=4 --publish 8000:8000 imageresizer
```

#### Cache clean schedule

By default, when purging the cache, the cache is cleaned every 24 hours starting from server launch, and images
older than 24 hours are deleted.

To change this:

* set the `CACHE_VALIDITY_S` environment variable for the duration which images should be cached (in seconds).
* set the `CACHE_CLEAN_INTERVAL_S` environment variable to specify the interval in seconds between cleaning tasks.

For example, to purge images older than one hour, every 2 minutes::

```bash
docker run --detach --env CACHE_VALIDITY_S=3600 --env CACHE_CLEAN_INTERVAL_S=120 --publish 8000:8000 imageresizer
```

#### Stopping the containers

To stop the running imageresizer containers:

```bash
for container in $(docker ps --filter ancestor=imageresizer --format="{{.ID}}"); do docker stop $container; done
```

To stop and delete all the imageresizer containers:

```bash
bash scripts/docker_remove_containers.bash
```

## Usage

Browse the api docs at http://127.0.0.1:8000/docs

Use the `resize` endpoint.

Example resizing the [GitHub logo](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png) to 50x100:

http://127.0.0.1:8000/resize?image_url=https%3A%2F%2Fgithub.githubassets.com%2Fimages%2Fmodules%2Flogos_page%2FGitHub-Mark.png&width=50&height=100

## Deleting old images

### Locally

```bash
python -m imageresizer.purge --max-age <age in seconds>
```

### Using docker

```bash
bash scripts/docker_purge_images.bash [max age in seconds (default is 86400)]
```

## Generated API documentation

You can browse the documentation at the following links:

* Running on the server:
    - Redoc: http://localhost:8000/redoc
    - Swagger: http://localhost:8000/docs
    - Open api doc: http://localhost:8000/openapi.json
* Static documentation:
    - Github pages: https://caarmen.github.io/image-resizer/
