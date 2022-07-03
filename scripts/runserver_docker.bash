docker build -t imageresizer .
docker run --detach --publish 8000:8000 imageresizer
