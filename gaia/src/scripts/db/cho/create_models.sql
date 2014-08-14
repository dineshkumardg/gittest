--
-- This file is _derived_ from ,create_models.sql being manually merged into this file.
--
-- -------------------------------------------
-- create the models for *ONE PROJECT* in GAIA
-- Note: each project has its own tablespace.
-- -------------------------------------------
--
-- To produce ,create_models.sql do:
-- cd ~/GIT_REPOS/gaia/src/scripts/dev
-- ./dump_models.sh
--
-- Manual merge needs to do the following (for sanities sake with all fields):
-- . add: SET default_tablespace...
-- . change (on qa tables): serial NOT NULL PRIMARY KEY, > bigserial NOT NULL PRIMARY KEY,
-- . change (on qa tables): integer NOT NULL > bigint NOT NULL,
-- . uncomment: -- ALTER
-- . only have one BEGIN ... COMMIT
--
-- NOTE: the serial > bigserial change is to ensure that a sequence is created and that it can cope with over 2147483647 (4 signed bytes).
--
BEGIN;
-- WARNING: THIS IS VERY IMPORTANT TO BE ADDED (is *not* included by django)
-- and *varies* per project .. be warned!
SET default_tablespace = cho_tablespace;

CREATE TABLE "django_content_type" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
)
;
CREATE TABLE "auth_permission" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
)
;
CREATE TABLE "auth_group_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("group_id", "permission_id")
)
;
CREATE TABLE "auth_group" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
)
;
ALTER TABLE "auth_group_permissions" ADD CONSTRAINT "group_id_refs_id_3cea63fe" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "auth_user_user_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "permission_id")
)
;
CREATE TABLE "auth_user_groups" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "group_id")
)
;
CREATE TABLE "auth_user" (
    "id" serial NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" boolean NOT NULL,
    "is_active" boolean NOT NULL,
    "is_superuser" boolean NOT NULL,
    "last_login" timestamp with time zone NOT NULL,
    "date_joined" timestamp with time zone NOT NULL
)
;
ALTER TABLE "auth_user_user_permissions" ADD CONSTRAINT "user_id_refs_id_f2045483" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_user_groups" ADD CONSTRAINT "user_id_refs_id_831107f1" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
-- The following references should be added but depend on non-existent tables:
ALTER TABLE "auth_permission" ADD CONSTRAINT "content_type_id_refs_id_728de91f" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "auth_permission_content_type_id" ON "auth_permission" ("content_type_id");
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" timestamp with time zone NOT NULL
)
;
CREATE INDEX "django_session_expire_date" ON "django_session" ("expire_date");
CREATE TABLE "django_admin_log" (
    "id" serial NOT NULL PRIMARY KEY,
    "action_time" timestamp with time zone NOT NULL,
    "user_id" integer NOT NULL,
    "content_type_id" integer,
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint CHECK ("action_flag" >= 0) NOT NULL,
    "change_message" text NOT NULL
)
;
-- The following references should be added but depend on non-existent tables:
ALTER TABLE "django_admin_log" ADD CONSTRAINT "content_type_id_refs_id_288599e6" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "django_admin_log" ADD CONSTRAINT "user_id_refs_id_c8665aa" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "django_admin_log_user_id" ON "django_admin_log" ("user_id");
CREATE INDEX "django_admin_log_content_type_id" ON "django_admin_log" ("content_type_id");
CREATE TABLE "item" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "dom_id" varchar(1022) NOT NULL,
    "dom_name" varchar(1022) NOT NULL,
    "is_live" boolean NOT NULL,
    "has_changed" boolean NOT NULL,
    "date" timestamp with time zone NOT NULL
)
;
CREATE TABLE "document" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "dom_id" varchar(1022) NOT NULL,
    "dom_name" varchar(1022) NOT NULL,
    "item_id" bigint NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "page" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "dom_id" varchar(1022) NOT NULL,
    "dom_name" varchar(1022) NOT NULL,
    "document_id" bigint NOT NULL REFERENCES "document" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "chunk_pages" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "chunk_id" bigint NOT NULL,
    "page_id" bigint NOT NULL REFERENCES "page" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("chunk_id", "page_id")
)
;
CREATE TABLE "chunk" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "dom_id" varchar(1022) NOT NULL,
    "dom_name" varchar(1022) NOT NULL,
    "document_id" bigint NOT NULL REFERENCES "document" ("id") DEFERRABLE INITIALLY DEFERRED,
    "is_binary" boolean NOT NULL
)
;
ALTER TABLE "chunk_pages" ADD CONSTRAINT "chunk_id_refs_id_7aa8e024" FOREIGN KEY ("chunk_id") REFERENCES "chunk" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "clip" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "dom_id" varchar(1022) NOT NULL,
    "dom_name" varchar(1022) NOT NULL,
    "page_id" bigint NOT NULL REFERENCES "page" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "link" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "dom_id" varchar(1022) NOT NULL,
    "dom_name" varchar(1022) NOT NULL,
    "document_id" bigint NOT NULL REFERENCES "document" ("id") DEFERRABLE INITIALLY DEFERRED,
    "chunk_id" bigint REFERENCES "chunk" ("id") DEFERRABLE INITIALLY DEFERRED,
    "page_id" bigint REFERENCES "page" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "asset_link" (
    "_link_ptr_id" bigserial NOT NULL PRIMARY KEY REFERENCES "link" ("id") DEFERRABLE INITIALLY DEFERRED,
    "asset_fname" varchar(512) NOT NULL
)
;
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
);
CREATE INDEX "document_item_id" ON "document" ("item_id");
CREATE INDEX "page_document_id" ON "page" ("document_id");
CREATE INDEX "chunk_document_id" ON "chunk" ("document_id");
CREATE INDEX "clip_page_id" ON "clip" ("page_id");
CREATE INDEX "link_document_id" ON "link" ("document_id");
CREATE INDEX "link_chunk_id" ON "link" ("chunk_id");
CREATE INDEX "link_page_id" ON "link" ("page_id");
CREATE TABLE "item_status" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "item_id" bigint NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "status" integer NOT NULL,
    "when" timestamp with time zone NOT NULL
)
;
CREATE TABLE "item_qa_activity" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL,
    "date" timestamp with time zone NOT NULL,
    "item_id" bigint NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "page_qa_activity" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL,
    "date" timestamp with time zone NOT NULL,
    "page_id" bigint NOT NULL REFERENCES "page" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "chunk_qa_activity" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL,
    "date" timestamp with time zone NOT NULL,
    "chunk_id" bigint NOT NULL REFERENCES "chunk" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "item_errors" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "item_id" bigint NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "when" timestamp with time zone NOT NULL,
    "err_type" varchar(32) NOT NULL,
    "err_msg" varchar(2048) NOT NULL
)
;
CREATE TABLE "ingest_error" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "provider_name" varchar(24) NOT NULL,
    "when" timestamp with time zone NOT NULL,
    "report" varchar(307200) NOT NULL
)
;
CREATE TABLE "document_final_id" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "final_id" varchar(128) NOT NULL,
    "document_id" bigint NOT NULL REFERENCES "document" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "page_final_id" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "final_id" varchar(128) NOT NULL,
    "page_id" bigint NOT NULL REFERENCES "page" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "chunk_final_id" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "final_id" varchar(128) NOT NULL,
    "chunk_id" bigint NOT NULL REFERENCES "chunk" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "clip_final_id" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "final_id" varchar(128) NOT NULL,
    "clip_id" bigint NOT NULL REFERENCES "clip" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "link_final_id" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "final_id" varchar(128) NOT NULL,
    "link_id" bigint NOT NULL REFERENCES "link" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "feed_file_items" (
    "id" serial NOT NULL PRIMARY KEY,
    "feedfile_id" integer NOT NULL,
    "item_id" bigint NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
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
CREATE INDEX "item_status_item_id" ON "item_status" ("item_id");
CREATE INDEX "item_qa_activity_item_id" ON "item_qa_activity" ("item_id");
CREATE INDEX "page_qa_activity_page_id" ON "page_qa_activity" ("page_id");
CREATE INDEX "chunk_qa_activity_chunk_id" ON "chunk_qa_activity" ("chunk_id");
CREATE INDEX "item_errors_item_id" ON "item_errors" ("item_id");
CREATE INDEX "document_final_id_document_id" ON "document_final_id" ("document_id");
CREATE INDEX "page_final_id_page_id" ON "page_final_id" ("page_id");
CREATE INDEX "chunk_final_id_chunk_id" ON "chunk_final_id" ("chunk_id");
CREATE INDEX "clip_final_id_clip_id" ON "clip_final_id" ("clip_id");
CREATE INDEX "asset_link_final_id_link_id" ON "asset_link_final_id" ("link_id");
CREATE INDEX "document_link_final_id_link_id" ON "document_link_final_id" ("link_id");

CREATE TABLE "asset_id_cache" (
    "asset_id" varchar(32) NOT NULL PRIMARY KEY
);

CREATE TABLE "m_codes" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "mcode" varchar(4) NOT NULL,
    "psmid" varchar(50) NOT NULL,
    "publication_title" varchar(250) NOT NULL
);

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

CREATE TABLE "language" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "psmid" varchar(50),
    "article_id" integer,
    "lang" varchar(50)
);

CREATE INDEX "language_psmid_id" ON "language" ("psmid");

CREATE TABLE "reject_reason" (
    "id" serial NOT NULL PRIMARY KEY,
    "item_id" bigint NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "reason" varchar(2000) NOT NULL,
    "who_id" bigint NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "when" timestamp with time zone NOT NULL);

COMMIT;
