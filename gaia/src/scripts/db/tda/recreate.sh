#!/bin/sh
PROJECT="TDA"
echo "WARNING: This will DELETE ***ALL*** the ${PROJECT} data from the database!"
set -x
# use this to force entry of password (otherwise use a ~/.pgpass file for development)
# For LIVE:...
#REQUIRE_PASSWORD="--password"
# For development:...
REQUIRE_PASSWORD=""
psql -U postgres ${REQUIRE_PASSWORD} -f drop.sql

#psql -U postgres ${REQUIRE_PASSWORD} -f ../shared/create_users.sql
psql -U postgres ${REQUIRE_PASSWORD} -f create_tablespace.sql
psql -U postgres ${REQUIRE_PASSWORD} -f create_db.sql

set +x
echo "NOTE: Use the gaia user from now on to ensure correct ownership/permissions on tables..."
set -x
psql -U gaia ${REQUIRE_PASSWORD} -l
psql -U gaia ${REQUIRE_PASSWORD} -d ${PROJECT} -f create_models.sql
psql -U gaia ${REQUIRE_PASSWORD} -d ${PROJECT} -f set_sequences.sql
