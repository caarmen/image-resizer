FROM python:3.10-slim

WORKDIR /app

COPY requirements/prod.txt requirements.txt

RUN pip install -r requirements.txt

COPY imageresizer imageresizer

CMD uvicorn --host 0.0.0.0 --port 8000 imageresizer.main:app