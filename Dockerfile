FROM python:3.10-slim

RUN apt-get update && apt-get --assume-yes install curl gpg

RUN curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list

WORKDIR /app

COPY requirements/prod.txt requirements.txt

RUN pip install -r requirements.txt

COPY imageresizer imageresizer

CMD CACHE_DIR=/var/cache/image-resizer uvicorn --host 0.0.0.0 --port 8000 --workers=${WORKER_COUNT:-1} imageresizer.main:app