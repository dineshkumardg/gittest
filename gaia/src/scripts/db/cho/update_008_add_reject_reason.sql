BEGIN;

CREATE TABLE "reject_reason" (
    "id" serial NOT NULL PRIMARY KEY,
    "item_id" bigint NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "reason" varchar(2000) NOT NULL,
    "who_id" bigint NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "when" timestamp with time zone NOT NULL);

COMMIT;