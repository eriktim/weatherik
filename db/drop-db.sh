#!/bin/sh

set -e

me=$(id -un)
if [ "$me" != "postgres" ]; then
  echo "Run this script as 'postgres'!" >&2
  exit 1
fi

echo "WARNING: This action will delete ALL your records."
echo -n "Do you wish to continue? (yes/no) "
read confirm

if [ "$confirm" != "yes" ]; then
  echo "Aborted." >&2
  exit 2
fi

dbname="weatherik"
user="weatherik_user"
pg_hba=$(ls /etc/postgresql/*/main/pg_hba.conf | tr -d '\n')

sed -i "/$user/d" ${pg_hba}
dropdb ${dbname} 2>/dev/null
dropuser ${user} 2>/dev/null
