docker build -t imageresizer .

host_cache_dir=/tmp/image-resizer/cache
host_log_dir=/tmp/image-resizer/logs
mkdir -p $host_cache_dir
mkdir -p $host_log_dir

container_log_dir=/var/log/image_resizer

docker run \
    --volume $host_cache_dir:/var/cache/image-resizer \
    --volume $host_log_dir:$container_log_dir \
    --detach \
    --publish 8000:8000 \
    --env WEB_CONCURRENCY=4 \
    --env LOG_FOLDER=$container_log_dir \
    imageresizer
