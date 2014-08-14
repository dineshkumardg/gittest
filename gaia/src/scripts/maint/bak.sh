#!/bin/bash

export PGPASSWORD=potatoes

/usr/bin/pg_dumpall -U postgres -f /GAIA/cho/postgres_dump/gaia_backup_$(date +%w).sql
/usr/bin/pg_dump -U postgres cho > /GAIA/cho/postgres_dump/cho_backup_$(date +%w).sql

# we also keep a copy on the network
/usr/bin/pg_dumpall -U postgres -f /mnt/UKDEV/POSTGRES_DB_DUMPS/gaia_backup_$(date +%w).sql
/usr/bin/pg_dump -U postgres cho > /mnt/UKDEV/POSTGRES_DB_DUMPS/cho_backup_$(date +%w).sql

