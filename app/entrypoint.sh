#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 2
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations service_transactions && python manage.py migrate

exec "$@"