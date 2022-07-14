git pull &&

python3 ../watchdog/telegram.py "Backend Update started"
echo "=========================================================="

# Get previous version of the container
PREVIOUS_CONTAINER=$(docker ps --format "table {{.ID}}  {{.Names}}  {{.CreatedAt}}" | grep backend | awk -F  "  " '{print $1}')
echo "Previous container: $PREVIOUS_CONTAINER"

# create new version of the container
echo "Creating new container..."
docker-compose -f ../docker-compose.prod.yml up -d --no-deps --scale backend=2  --build backend
sleep 10
echo "New container created"

# kill old container
echo "Killing old container..."
docker kill -s SIGTERM $PREVIOUS_CONTAINER
sleep 1
docker rm -f $PREVIOUS_CONTAINER
echo "Old container killed"

# Refresh to the old config
echo "Refreshing to the old config..."
docker-compose -f ../docker-compose.prod.yml  up -d --no-deps --scale backend=1 --no-recreate backend
echo "Refreshed"

# Restart the nginx container
echo "Restarting nginx..."
docker-compose -f ../docker-compose.prod.yml  stop nginx
docker-compose -f ../docker-compose.prod.yml  up -d --no-deps nginx
echo "Nginx restarted"

echo "Cleanup..."
docker system prune -f
docker image prune -f
docker volume prune -f
docker network prune -f
docker container prune -f
docker container ls -a
echo "Cleanup done"

python3 ../watchdog/telegram.py "Backend updated"
echo "=========================================================="
