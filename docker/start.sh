#!/bin/bash

set -e

while ! (timeout 3 bash -c "</dev/tcp/${POSTGRES_HOST_PDATA}/${POSTGRES_PORT_PDATA}") &> /dev/null;

do
  echo waiting for PostgreSQL to start...;
  sleep 3;
done;

echo "starting $APP_NAME";

if [[ ${APP_NAME} == 'weather_app' ]]
  then
    ./manage.py makemigrations
    ./manage.py migrate  --no-input --traceback
    ./manage.py collectstatic --no-input
    echo yes | ./manage.py test
    # if [[  ${DEBUG} == '1' || ${DEBUG} == 'true' ]]
    #   then
    ./manage.py runserver 0.0.0.0:8000
    # else
    #     gunicorn --bind 0.0.0.0:8000 core.wsgi
    # fi
  fi
