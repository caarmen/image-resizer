for container in $(docker ps --all --filter ancestor=imageresizer --format="{{.ID}}")
do
  echo "purging images in container $container"
  docker exec --env CACHE_DIR=/var/cache/image-resizer -it $container python -m imageresizer.purge --max-age ${1:-86400}
done

