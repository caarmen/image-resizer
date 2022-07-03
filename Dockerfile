FROM python:3.10-slim

ARG PORT=8000
ENV PORT $PORT
WORKDIR /app

COPY requirements/prod.txt requirements.txt

RUN pip install -r requirements.txt

COPY imageresizer imageresizer

CMD uvicorn --host 0.0.0.0 --port $PORT imageresizer.main:app