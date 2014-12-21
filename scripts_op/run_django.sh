#!/bin/bash

if [ "${BASH_ARGC}" == 2 ]
then
  ini_filename="${BASH_ARGV[1]}"
  port="${BASH_ARGV[0]}"
elif [ "${BASH_ARGC}" == 1 ]
then
  ini_filename="${BASH_ARGV[0]}"
  port="12345"
else
  echo "usage: run_django.sh [ini_filename] [port=12345]"
  exit 0
fi

. __/bin/activate

python manage.py syncdb

python manage.py collectstatic --noinput

uwsgi --module f6a_tw_backend.main_django:application --http 0.0.0.0:${port} --gevent 100 --set ini=${ini_filename} --set port=${port} -H __
