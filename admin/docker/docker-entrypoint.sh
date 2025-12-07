#!/bin/bash
set -e

DEV_USERNAME=user
DEV_PASSWORD=hackme
DEV_EMAIL=admin@admin.ru
PORT=${PORT:-8001}


# Start server in dev mode
dev() {
  if [[ "${MIGRATION_ENABLED}" == "true" ]]; then
    echo "Starting migrations to all database";
    python manage.py migrate || true;
  fi
  echo "Collecting static files..."
  python3 manage.py collectstatic --no-input
  echo "Starting server in dev mode..."
  DEBUG=${DEBUG:-True}
  echo "!!! DEV mode. DEBUG=${DEBUG}"
  if DJANGO_SUPERUSER_USERNAME=${DEV_USERNAME} \
  DJANGO_SUPERUSER_PASSWORD=${DEV_PASSWORD} \
  DJANGO_SUPERUSER_EMAIL=${DEV_EMAIL} \
  python3 manage.py createsuperuser --no-input ; then
    echo "username: ${DEV_USERNAME}"
    echo "password: ${DEV_PASSWORD}"
  fi

  DEBUG=${DEBUG} exec python3 manage.py runserver 0.0.0.0:${PORT}
}


server() {

  export HOST=${APP_HOST:-0.0.0.0}
  export PORT=${APP_PORT:-8080}
  export LOG_LEVEL=${LOG_LEVEL:-info}
  export WORKERS_NUM=${WORKERS_NUM:-1}

  exec gunicorn --bind ${HOST}:${PORT} --workers ${WORKERS_NUM} --timeout 121 wsgi

}

start-reload() {
  export HOST=${APP_HOST:-0.0.0.0}
  export PORT=${APP_PORT:-8000}
  export WORKERS_NUM=${WORKERS_NUM:-2}

  exec gunicorn --bind ${HOST}:${PORT} --workers ${WORKERS_NUM} wsgi
}


migrate() {
  export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-infra.settings}
  case "${MIGRATION_ENABLED}" in
  true)
    echo "Starting migration"
    exec python manage.py migrate
    ;;
  fake)
    echo "Starting fake migration"
    exec python manage.py migrate --fake
    ;;
  false)
    echo "Disable migration"
    exit 0
    ;;
  *)
    echo "Set env MIGRATION_ENABLED to true, fake or false"
    exit 1
    ;;
  esac
}

run-tests() {
  export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-infra.settings}
  export STAGE=ci_runtests
  pytest tests/integration -vv
}

help() {
  echo "Editorial collections admin Docker."
  echo ""
  echo "Usage:"
  echo ""
  echo "server -- start backend"
  echo "migrate -- start database migration"
  echo ""
  echo "dev -- Create admin user and start server in dev mode on port 8001"
  echo "test -- Run tests in docker compose"
}

case "$1" in
server)
  shift
  server
  ;;
help)
  shift
  help
  ;;
start-reload)
  shift
  start-reload
  ;;
migrate)
  shift
  migrate
  ;;
dev)
  shift
  dev
  ;;
run-tests)
  shift
  run-tests
  ;;
*)
  exec "$@"
  ;;
esac
