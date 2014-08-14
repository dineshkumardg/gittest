-- usage:
-- psql -U postgres cho -f update_003_bigint_to_bigserial.sql
-- psql -U postgres -p <port> <db> -f update_003_bigint_to_bigserial.sql

-- NOTE: 
-- 1. When you issue an ALTER TABLE in PostgreSQL it will take
-- an ACCESS EXCLUSIVE lock that blocks everything including SELECT. 
-- (from: http://dba.stackexchange.com/questions/27153/alter-table-on-live-production-databases)
-- (so we think we *can* do this on a live, running database)
--
-- 2. Its possible that for an ALTER that we don't need to wrap it in a transaction?

BEGIN;
ALTER TABLE "document_final_id" ALTER COLUMN "document_id" TYPE bigint;
ALTER TABLE "page_final_id" ALTER COLUMN "page_id" TYPE bigint;
ALTER TABLE "chunk_final_id" ALTER COLUMN "chunk_id" TYPE bigint;
ALTER TABLE "clip_final_id" ALTER COLUMN "clip_id" TYPE bigint;
ALTER TABLE "link_final_id" ALTER COLUMN "link_id" TYPE bigint;
ALTER TABLE "feed_file_items" ALTER COLUMN "item_id" TYPE bigint;

-- This part of script DOES NOT not need to be run (thought it causes no harm if it is), as Postgres automatically converts bigserial foreign keys into bigint's!
--
-- You can observe this behaviour by dumping the database (schame only via -s) before you run this script and after you run this script.
--
-- 0. Assuming create_models.sql @ 8cfe26d9682776771c720226530229c89dc0aace is the schema inside the <db>
-- 1. pg_dump -U postgres -p <port> -s -c <db> > schema-8cfe26d9682776771c720226530229c89dc0aace.sql
-- 2. psql -U postgres -p <port> <db> -f update_003_bigint_to_bigserial.sql
-- 3. pg_dump -U postgres -p <port> -s -c <db> > schema-update_003_bigint_to_bigserial.sql
-- 4. diff schema-8cfe26d9682776771c720226530229c89dc0aace.sql schema-update_003_bigint_to_bigserial.sql
--
-- NOTE the alter does not affect REFERENCES commands in create_models.sql
--
ALTER TABLE "document" ALTER COLUMN "item_id" TYPE bigint;
ALTER TABLE "page" ALTER COLUMN "document_id" TYPE bigint;
ALTER TABLE "chunk_pages" ALTER COLUMN "chunk_id" TYPE bigint;
ALTER TABLE "chunk_pages" ALTER COLUMN "page_id" TYPE bigint;
ALTER TABLE "chunk" ALTER COLUMN "document_id" TYPE bigint;
ALTER TABLE "chunk_pages" ALTER COLUMN "page_id" TYPE bigint;
ALTER TABLE "link" ALTER COLUMN "document_id" TYPE bigint;
ALTER TABLE "item_status" ALTER COLUMN "item_id" TYPE bigint;
ALTER TABLE "item_qa_activity" ALTER COLUMN "item_id" TYPE bigint;
ALTER TABLE "page_qa_activity" ALTER COLUMN "page_id" TYPE bigint;
ALTER TABLE "chunk_qa_activity" ALTER COLUMN "chunk_id" TYPE bigint;
ALTER TABLE "item_errors" ALTER COLUMN "item_id" TYPE bigint;
COMMIT;
