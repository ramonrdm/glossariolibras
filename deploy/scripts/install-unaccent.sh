#!/bin/sh

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<EOF
create EXTENSION unaccent;
EOF