BEGIN;

CREATE TABLE "language" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "psmid" varchar(50),
    "article_id" integer,
    "lang" varchar(50)
);

CREATE INDEX "language_psmid_id" ON "language" ("psmid");

COMMIT;