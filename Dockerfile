FROM python:3.10-slim

WORKDIR /app

COPY requirements/prod.txt requirements.txt

RUN pip install -r requirements.txt

COPY imageresizer imageresizer

CMD CACHE_DIR=/var/cache/image-resizer python -m imageresizer.main