FROM python:3.10-slim

WORKDIR /app

COPY requirements/prod.txt requirements.txt

RUN pip install -r requirements.txt

COPY imageresizer imageresizer

CMD CACHE_DIR=/var/cache/image-resizer uvicorn --host 0.0.0.0 --port 8000 --workers=${WORKER_COUNT:-1} imageresizer.main:app