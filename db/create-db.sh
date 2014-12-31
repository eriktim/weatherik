#!/bin/sh

set -e

me=$(id -un)
if [ "$me" != "postgres" ]; then
  echo "Run this script as 'postgres'!" >&2
  exit 1
fi

dbname="weatherik"
user="weatherik_user"
password="weatherik_password"
pg_hba=$(ls /etc/postgresql/*/main/pg_hba.conf | tr -d '\n')

createuser --no-superuser --no-createrole --createdb ${user}
createdb -E UTF8 -O ${user} ${dbname}
echo "ALTER USER ${user} WITH PASSWORD '${password}';" | psql -d ${dbname}>/dev/null
echo "host\t${dbname}\t${user}\t127.0.0.1/32\tmd5" >> ${pg_hba}
psql -d ${dbname} >/dev/null < db.sql
