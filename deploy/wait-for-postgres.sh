#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

postgres

until docker exec -it db_postgres_container psql -U libras; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd