#!/bin/sh
set -e

until psql $DATABASE_URL -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

if [ "$1" = '/venv/bin/uwsgi' ]; then
    /venv/bin/python manage.py migrate --noinput
    /venv/bin/python manage.py loaddata fixt.json
fi

exec "$@"
