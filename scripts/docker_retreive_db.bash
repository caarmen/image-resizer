for container in $(docker ps --all --filter ancestor=imageresizer --format="{{.ID}}")
do
  target=/tmp/image-resizer-$container.db
  docker cp $container:/app/image-resizer.db $target
  echo "Fetched $target"
done

