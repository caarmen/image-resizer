docker build -t imageresizer .
docker run --detach --publish 8000:8000 --env WEB_CONCURRENCY=4 imageresizer
