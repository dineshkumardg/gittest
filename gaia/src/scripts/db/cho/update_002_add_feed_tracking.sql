-- usage:
-- psql -U postgres cho -f update_002*.sql

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
    
CREATE TABLE "feed_file_items" (
    "id" serial NOT NULL PRIMARY KEY,
    "feedfile_id" integer NOT NULL,
    "item_id" integer NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("feedfile_id", "item_id")
)
;
CREATE TABLE "feed_file" (
    "id" serial NOT NULL PRIMARY KEY,
    "fname" varchar(64) NOT NULL,
    "when" timestamp with time zone NOT NULL,
    "group" varchar(64) NOT NULL,
    "num_docs" varchar(64) NOT NULL
)
;
ALTER TABLE "feed_file_items" ADD CONSTRAINT "feedfile_id_refs_id_75f5ebec" FOREIGN KEY ("feedfile_id") REFERENCES "feed_file" ("id") DEFERRABLE INITIALLY DEFERRED;

-- NOTE: we did the follwiong separately on ukandgaia07
-- TODO: how to set the owner WHEN WE CREATE the table above...
-- psql -U postgres cho -f ,alter.sql
ALTER TABLE feed_file OWNER TO gaia;
ALTER TABLE feed_file_id_seq OWNER TO gaia;
ALTER TABLE feed_file_items OWNER TO gaia;
ALTER TABLE feed_file_items_id_seq OWNER TO gaia;

COMMIT;
