--
-- to backup postgres:
-- pg_dumpall -U postgres -f ~/Desktop/new_dump_18_07.sql
--
-- to backup just a database:
-- pg_dump -U postgres -p 5433 cho > db.bak
--
-- to restore jsut a database:
-- psql -U gaia -d cho -f db.bak
--
-- to restore postgres:
-- psql -U postgres -f ~/Desktop/new_dump_18_07.sql
--
-- apply this patch (NOTE: tables need to be created as correct user):
-- psql -U gaia -d cho -f ~/GIT_REPOS/gaia/src/scripts/db/cho/update_005_add_m_codes.sql
--
-- NOTE: 
-- 1. When you issue an ALTER TABLE in PostgreSQL it will take
-- an ACCESS EXCLUSIVE lock that blocks everything including SELECT. 
-- (from: http://dba.stackexchange.com/questions/27153/alter-table-on-live-production-databases)
-- (so we think we *can* do this on a live, running database)
--

BEGIN;

CREATE TABLE "m_codes" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "mcode" varchar(4) NOT NULL,
    "psmid" varchar(50) NOT NULL,
    "publication_title" varchar(250) NOT NULL
)
;

COMMIT;