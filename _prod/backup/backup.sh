BACKEND_CONTAINER=$(docker ps --format "table {{.ID}}  {{.Names}}  {{.CreatedAt}}" | grep backend | awk -F  "  " '{print $1}')
#BACKEND_CONTAINER=$(docker ps --format "table {{.ID}}  {{.Names}}  {{.CreatedAt}}" | grep website_web | awk -F  "  " '{print $1}')

echo "Backup of the backend container $BACKEND_CONTAINER"
docker exec -it "$BACKEND_CONTAINER" python  manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > dump.json
echo "Dump created"


echo "Upload to google drive"
# if a name is given, use it, otherwise use the current date
if [ -z "$1" ]
  then
    python3 ./backup.py dump.json "$(date +%Y-%m-%d_%H-%M-%S)_backup.json"
  else
        python3 ./backup.py dump.json "$1"
fi

python3 ../../watchdog/telegram.py "BackUp Done !"
