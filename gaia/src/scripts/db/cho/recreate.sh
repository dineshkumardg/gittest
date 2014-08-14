#!/bin/sh
# This is a convenience script for development and initial live server setup only.

DB="cho"
#LOCAL_DB_PORT=5433

echo "WARNING: This script will DELETE ***ALL*** the '${DB}' data from the database!"
echo 
echo 'NOTE: script assumes:'
echo ". '${DB}_tablespace' exists"
echo '. 'gaia' is a database user'
echo '. create_models.sql correctly merged'
echo '. you know the passwords for the 'postgres' and 'gaia' database users'
echo ". no one is using the '${DB}' database"
echo 
read -p "Press [Enter] key to carry on..."

# could use ~/.pgpass file OR export PGPASSWORD for password provision

#PGPASSWORD=""
# drop db TODO rename
psql -U postgres -p ${LOCAL_DB_PORT} -f drop.sql
#psql -U postgres -f ../shared/create_users.sql
#psql -U postgres -f create_tablespace.sql
psql -U postgres -f create_db.sql

echo "NOTE: Using gaia user to ensure correct ownership/permissions on tables..."
#PGPASSWORD=""
psql -U gaia -d ${DB} -f create_models.sql
