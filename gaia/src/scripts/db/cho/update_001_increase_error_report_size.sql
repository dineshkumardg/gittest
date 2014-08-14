-- usage:
-- psql -U postgres -p <port> <db> -f update_001_increase_error_report_size.sql

-- to backup table prior: 
-- pg_dump -U postgres -p <port> -c <db> -t ingest_error > ingest_error.backup
-- 
-- to restore table:
-- psql -U postgres -p <port> <db> -f ingest_error.backup

-- NOTE: 
-- 1. When you issue an ALTER TABLE in PostgreSQL it will take
-- an ACCESS EXCLUSIVE lock that blocks everything including SELECT. 
-- (from: http://dba.stackexchange.com/questions/27153/alter-table-on-live-production-databases)
-- (so we think we *can* do this on a live, running database)
--
-- 2. Its possible that for an ALTER that we don't need to wrap it in a transaction?

BEGIN;
-- VARCHAR == character varying - http://www.postgresql.org/docs/9.2/static/datatype.html
ALTER TABLE ingest_error ALTER COLUMN report TYPE VARCHAR(307200);  -- 300k
COMMIT;
