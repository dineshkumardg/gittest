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
-- psql -U gaia -d cho -f ~/GIT_REPOS/gaia/src/scripts/db/cho/update_004_add_related_docs.sql
--
-- NOTE: 
-- 1. When you issue an ALTER TABLE in PostgreSQL it will take
-- an ACCESS EXCLUSIVE lock that blocks everything including SELECT. 
-- (from: http://dba.stackexchange.com/questions/27153/alter-table-on-live-production-databases)
-- (so we think we *can* do this on a live, running database)
--

BEGIN;

ALTER TABLE "link" ADD COLUMN "chunk_id" bigint REFERENCES "chunk" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "link" ADD COLUMN "page_id" bigint REFERENCES "page" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE "asset_link" (
    "_link_ptr_id" bigserial NOT NULL PRIMARY KEY REFERENCES "link" ("id") DEFERRABLE INITIALLY DEFERRED,
    "asset_fname" varchar(512) NOT NULL
)
;

-- TUSH: MIGRATE any link asset ids (from link_final_id to asset_link_final_id) ...
-- TODO: rm table (?) link_final_id AND migrate data into asset_link_final_id? + any related index link_final_id_link_id? 

CREATE TABLE "asset_link_final_id" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "final_id" varchar(128) NOT NULL,
    "link_id" bigint NOT NULL REFERENCES "asset_link" ("_link_ptr_id") DEFERRABLE INITIALLY DEFERRED
)
;

CREATE TABLE "document_link" (
    "_link_ptr_id" bigserial NOT NULL PRIMARY KEY REFERENCES "link" ("id") DEFERRABLE INITIALLY DEFERRED,
    "unresolved_target_item" varchar(1022) NOT NULL,
    "unresolved_target_chunk" varchar(1022) NOT NULL,
    "unresolved_target_page" varchar(1022) NOT NULL
)
;

CREATE TABLE "document_link_final_id" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "final_id" varchar(128) NOT NULL,
    "link_id" bigint NOT NULL REFERENCES "document_link" ("_link_ptr_id") DEFERRABLE INITIALLY DEFERRED
)
;

CREATE INDEX "link_chunk_id" ON "link" ("chunk_id");
CREATE INDEX "link_page_id" ON "link" ("page_id");
CREATE INDEX "asset_link_final_id_link_id" ON "asset_link_final_id" ("link_id");
CREATE INDEX "document_link_final_id_link_id" ON "document_link_final_id" ("link_id");

--
-- the primary keys get sequences added to them automatically
-- 
CREATE SEQUENCE asset_link_final_id_link_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE asset_link_final_id_link_id_seq OWNER TO gaia; 
ALTER SEQUENCE asset_link_final_id_link_id_seq OWNED BY asset_link._link_ptr_id;

CREATE SEQUENCE document_link_final_id_link_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE document_link_final_id_link_id_seq OWNER TO gaia; 
ALTER SEQUENCE document_link_final_id_link_id_seq OWNED BY document_link._link_ptr_id;

COMMIT;
