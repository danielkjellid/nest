#!/bin/bash
set -e

if [ "$1" = 'start' ]; then
  exec bash -c "poetry run python cli build && poetry run gunicorn nest.wsgi:application ${*:2}"
fi

if [ "$1" = 'python' ]; then
    exec poetry run python ${*:2}
fi

if [ "$1" = 'gunicorn' ]; then
    exec poetry run gunicorn nest.wsgi:application ${*:2}
fi

if [ "$1" = 'migrate' ]; then
    exec poetry run python manage.py migrate ${*:2}
fi

if [ "$1" = 'shell' ]; then
    exec poetry run python manage.py shell ${*:2}
fi

if [ "$1" = 'shell_plus' ]; then
    exec poetry run python manage.py shell_plus ${*:2}
fi

if [ "$1" = 'dbshell' ]; then
    exec poetry run python manage.py dbshell ${*:2}
fi

exec "$@"