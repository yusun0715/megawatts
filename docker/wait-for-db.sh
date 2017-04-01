#!/usr/bin/env bash
set -e

MYARGS="$1"
HOST=${MYARGS%:*}  # Get everything before `:`
PORT=${MYARGS##*:} # Get everything after `:`

shift
cmd="$@"

until psql postgres --host=$HOST --port=$PORT -U "postgres" -c '\l' >> /dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

exec $cmd