for container in $(docker ps --all --filter ancestor=imageresizer --format="{{.ID}}")
do
  echo "stopping container $container"
  docker stop $container
  docker rm $container
done 

for container in $(docker ps --all --filter ancestor=ghcr.io/caarmen/image-resizer --format="{{.ID}}")
do
  echo "stopping container $container"
  docker stop $container
  docker rm $container
done

