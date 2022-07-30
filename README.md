# Image resizer

An endpoint, using Fast API, that allows resizing an image.

[<img src="https://img.shields.io/badge/license-MIT-lightgrey.svg?maxAge=2592000">](https://github.com/caarmen/image-resizer/blob/main/LICENSE.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[<img src="https://github.com/caarmen/image-resizer/actions/workflows/tests.yml/badge.svg">](https://github.com/caarmen/image-resizer/actions?query=workflow%3A%22Run+tests%22++)

## TLDR quickstart

To run the server in a docker container, and have access to logs and cached data on the host
inside `/tmp/image-resizer`, use the Docker container hosted on Github packages:

```bash
docker pull ghcr.io/caarmen/image-resizer:latest

mkdir -p /tmp/image-resizer/cache
mkdir -p /tmp/image-resizer/logs

docker run \
    --volume /tmp/image-resizer/cache:/var/cache/image-resizer \
    --volume /tmp/image-resizer/logs:/var/log/image-resizer \
    --detach \
    --publish 8000:8000 \
    --env WEB_CONCURRENCY=4 \
    --env CACHE_VALIDITY_S=86400 \
    --env CACHE_CLEAN_INTERVAL_S=86400 \
    ghcr.io/caarmen/image-resizer
```

Then resize your first image here:

http://localhost:8000/resize?image_url=https://github.githubassets.com/images/modules/logos_page/Octocat.png&height=300&width=100&image_format=webp

## Building and running the server from sources

### Running the server locally

```bash
git clone https://github.com/caarmen/image-resizer.git
cd image-resizer
# optional: command to create virtual environment
pip install -r requirements/prod.txt
python -m imageresizer.main
```

### Building the docker image

```bash
git clone https://github.com/caarmen/image-resizer.git
cd image-resizer
docker build -t imageresizer .
docker run --detach --publish 8000:8000 imageresizer
```

## Server configuration options

The following options are valid whether you downloaded the image from Github packages, built the Docker image locally,
or are running the server directly on your machine.

The examples specify the image from Github packages `ghcr.io/caarmen/image-resizer`. If you built the image locally,
use `imageresizer` instead.

#### Cache and log folders

By default, the server stores the cache data and logs in the root of the project when run locally, and in
`/var/cache/image-resizer` and `/var/log/image-resizer` in the Docker container.

You can change the location of the cache and logs locations with the `CACHE_DIR` and `LOG_DIR` environment variables.

For example, to store cache and logs in `/tmp/image-resizer/cache` and `/tmp/image-resizer/logs`:

Docker:

```bash
docker run --detach --volume /tmp/image-resizer/cache:/var/cache/image-resizer --volume /tmp/image-resizer/logs:/var/log/image-resizer --publish 8000:8000 ghcr.io/caarmen/image-resizer
```

Local:

```bash
CACHE_DIR=/tmp/image-resizer/cache LOG_DIR=/tmp/image-resizer/logs python -m imageresizer.main
```

#### Worker count

By default, the server runs with one worker. To change this, specify the number of workers with the
`WEB_CONCURRENCY` environment variable. For example, to set 4 workers:

Docker:

```bash
docker run --detach --env WEB_CONCURRENCY=4 --publish 8000:8000 ghcr.io/caarmen/image-resizer
```

Local:

```bash
WEB_CONCURRENCY=4 python -m imageresizer.main
```

#### Cache clean schedule

By default, when purging the cache, the cache is cleaned every 24 hours starting from server launch, and images
older than 24 hours are deleted.

To change this:

* set the `CACHE_VALIDITY_S` environment variable for the duration which images should be cached (in seconds).
* set the `CACHE_CLEAN_INTERVAL_S` environment variable to specify the interval in seconds between cleaning tasks.

For example, to purge images older than one hour, every 2 minutes::

Docker:

```bash
docker run --detach --env CACHE_VALIDITY_S=3600 --env CACHE_CLEAN_INTERVAL_S=120 --publish 8000:8000 ghcr.io/caarmen/image-resizer
```

Local:

```bash
CACHE_VALIDITY_S=3600 CACHE_CLEAN_INTERVAL_S=120 python -m imageresizer.main
```

#### Server port

By default, the server runs on port 8000. To set it to run on a different port, like `8102` for example:

Docker:

```bash
docker run --detach --publish 8102:8000 ghcr.io/caarmen/image-resizer
```

Local:

```bash
UVICORN_PORT=8102 python -m imageresizer.main
```

#### Generated documentation urls

The following generated documentation urls are exposed. They can be disabled by unsetting their
environment variables.

| Documentation type | Environment variable | Default value |
|--------------------|----------------------|---------------|
| OpenAPI json       | `OPENAPI_URL`        | /openapi.json |
| ReDoc              | `REDOC_URL`          | /redoc        |
| Swagger UI         | `DOCS_URL`           | /docs         |

Example to disable all documentation urls:

Docker:

```bash
docker run --detach --env OPENAPI_URL= --env REDOC_URL= --env DOCS_URL= --publish 8000:8000 ghcr.io/caarmen/image-resizer
```

Local:

```bash
OPENAPI_URL= REDOC_URL= DOCS_URL= python -m imageresizer.main
```

#### Supported image url schemas

By default, only the https schema is allowed for image urls. To change this, set the `SUPPORTED_IMAGE_URL_SCHEMAS`
environment variable.

For example, to support both https and http:

Docker:

```bash
docker run --env SUPPORTED_IMAGE_URL_SCHEMAS='["https","http"]' --detach --publish 8000:8000 ghcr.io/caarmen/image-resizer
```

Local:

```bash
SUPPORTED_IMAGE_URL_SCHEMAS='["https","http"]' python -m imageresizer.main
```

#### Allowed and denied domains

By default, no restrictions are placed on the domains of image urls. To specifically deny a list of domains, or to
specifically only allow a list of domains, set the `DENIED_DOMAINS` or `ALLOWED_DOMAINS` environment variables.

For example, to ban resizing images on baddomain.com:

Docker:

```bash
docker run --env DENIED_DOMAINS='["baddomain.com"]' --detach --publish 8000:8000 ghcr.io/caarmen/image-resizer
```

Local:

```bash
DENIED_DOMAINS='["baddomain.com"]' python -m imageresizer.main
```

#### Stopping the containers (Docker only)

To stop the running imageresizer containers:

```bash
for container in $(docker ps --filter ancestor=ghcr.io/caarmen/image-resizer --format="{{.ID}}"); do docker stop $container; done
```

To stop and delete all the imageresizer containers, a utility script is provided in this repository:

```bash
bash scripts/docker_remove_containers.bash
```

## API Usage

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
