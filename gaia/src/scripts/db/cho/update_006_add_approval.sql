--
-- to backup postgres:
-- pg_dumpall -U postgres -f ~/Desktop/new_dump_18_07.sql
--
-- to backup just a database:
-- pg_dump -U postgres -p 5433 cho > db.bak
--
-- to restore just a database:
-- psql -U gaia -d cho -f db.bak
--
-- to restore postgres:
-- psql -U postgres -f ~/Desktop/new_dump_18_07.sql
--
-- apply this patch (NOTE: tables need to be created as correct user):
-- psql -U gaia -d cho -f ~/GIT_REPOS/gaia/src/scripts/db/cho/update_006_add_approval.sql
--

BEGIN;

CREATE TABLE "approval" (
    "id" serial NOT NULL PRIMARY KEY,
    "item_id" bigint NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "approved" boolean NOT NULL,
    "notes" varchar(250) NOT NULL,
    "who_id" bigint NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "when" timestamp with time zone NOT NULL
);

CREATE INDEX "approval_item_id" ON "approval" ("item_id");
CREATE INDEX "approval_who_id" ON "approval" ("who_id");

COMMIT;