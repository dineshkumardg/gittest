-- This file is _derived_ from ../,create_models.sql which can be re-generated
-- by running ../gaia_web/dump_models.sh. This then has to be *merged* into here.
--
-- -------------------------------------------
-- create the models for *ONE PROJECT* in GAIA
-- Note: each project has its own tablespace.
-- -------------------------------------------
--
-- WARNING!
-- data-type changes:
-- 1. datetime has been changed to timestamp as the data type in this file (for newer postgres)
--
-- 2. *Some* of the primary keys  have been changed to use BIGSERIAL instead of integer, ie:
--      "id" integer NOT NULL PRIMARY KEY, has beeen changed to:
--      "id" BIGSERIAL NOT NULL PRIMARY KEY
--    to ensure that a sequence is created and that it can cope with over 2147483647 (4 signed bytes).
--    Hence, also, references to that column have been changed from integer to bigint, eg:
--    "batch_id" integer NOT NULL,
--    "batch_id" bigint NOT NULL,
-- 
-- 3. varchar(1) has been changed (optimised) to char(1) - *NOT* (was in gaia dawn..?).

BEGIN;
-- WARNING: THIS IS VERY IMPORTANT TO BE ADDED (is *not* included by django)
-- and *varies* per project .. be warned!
SET default_tablespace = tda_tablespace;


-- TODO ==============================================
    -- "article_id" integer NOT NULL,
-- CREATE TABLE "article_categories" (
    --"id" serial NOT NULL PRIMARY KEY,
    --"article_id" bigint NOT NULL,
    --"category_id" bigint NOT NULL REFERENCES "category" ("id") DEFERRABLE INITIALLY DEFERRED,
    --UNIQUE ("article_id", "category_id")
--)
-- TODO ==============================================

CREATE TABLE "django_content_type" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
)
;
COMMIT;
BEGIN;
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
ALTER TABLE "auth_user_user_permissions" ADD CONSTRAINT "user_id_refs_id_dfbab7d" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_user_groups" ADD CONSTRAINT "user_id_refs_id_7ceef80f" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "auth_message" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "message" text NOT NULL
)
;
-- The following references should be added but depend on non-existent tables:
ALTER TABLE "auth_permission" ADD CONSTRAINT "content_type_id_refs_id_728de91f" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "auth_permission_content_type_id" ON "auth_permission" ("content_type_id");
CREATE INDEX "auth_message_user_id" ON "auth_message" ("user_id");
COMMIT;
BEGIN;
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" timestamp with time zone NOT NULL
)
;
CREATE INDEX "django_session_expire_date" ON "django_session" ("expire_date");
COMMIT;
BEGIN;
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
COMMIT;
BEGIN;
CREATE TABLE "config" (
    "id" serial NOT NULL PRIMARY KEY,
    "project_code" varchar(16) NOT NULL
)
;
    -- "id" serial NOT NULL PRIMARY KEY,
CREATE TABLE "item" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "name" varchar(250) NOT NULL UNIQUE,
    "mcode" varchar(4) NOT NULL,
    "total_pages" integer NOT NULL,
    "status" integer NOT NULL
)
;
CREATE TABLE "item2" (
    "dataitem_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "lang" varchar(250) NOT NULL,
    "full_title" varchar(250) NOT NULL,
    "display_title" varchar(250) NOT NULL,
    "pub_date_start" date NOT NULL,
    "pub_date_end" date NOT NULL,
    "imprint_full" varchar(250) NOT NULL,
    "imprint_publisher" varchar(250) NOT NULL,
    "collation" varchar(250) NOT NULL,
    "psm_id" varchar(64) NOT NULL
)
;
;
    -- "id" serial NOT NULL PRIMARY KEY,
    -- "item_id" integer NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
CREATE TABLE "page" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "name" varchar(250) NOT NULL UNIQUE,
    "item_id" bigint NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "pgref" integer NOT NULL
)
;
CREATE TABLE "clip" (
    "id" serial NOT NULL PRIMARY KEY,
    "coordinates" varchar(64) NOT NULL,
    "page_id" integer NOT NULL REFERENCES "page" ("id") DEFERRABLE INITIALLY DEFERRED,
    "clipref" integer NOT NULL
)
;
    -- "article_id" integer NOT NULL,
CREATE TABLE "article_clips" (
    "id" serial NOT NULL PRIMARY KEY,
    "article_id" bigint NOT NULL,
    "clip_id" integer NOT NULL REFERENCES "clip" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("article_id", "clip_id")
)
;
    -- "id" serial NOT NULL PRIMARY KEY,
    -- "item_id" integer NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
CREATE TABLE "article" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "name" varchar(250) NOT NULL UNIQUE,
    "item_id" bigint NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
ALTER TABLE "article_clips" ADD CONSTRAINT "article_id_refs_id_99bdc9f" FOREIGN KEY ("article_id") REFERENCES "article" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "qa_illustration" (
    "id" serial NOT NULL PRIMARY KEY,
    "il_type" varchar(32) NOT NULL,
    "caption" text NOT NULL,
    "clip_id" integer NOT NULL REFERENCES "clip" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "meeting" (
    "dataitem2_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "item2" ("dataitem_ptr_id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "pamphlet" (
    "dataitem2_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "item2" ("dataitem_ptr_id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "report" (
    "dataitem2_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "item2" ("dataitem_ptr_id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "conference_series" (
    "dataitem2_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "item2" ("dataitem_ptr_id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "discussion_paper" (
    "dataitem2_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "item2" ("dataitem_ptr_id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "briefing_paper" (
    "dataitem2_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "item2" ("dataitem_ptr_id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "bound_volume" (
    "dataitem2_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "item2" ("dataitem_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "citation_full_title" varchar(150) NOT NULL
)
;
CREATE TABLE "journal_issue" (
    "dataitem2_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "item2" ("dataitem_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "volume" varchar(32) NOT NULL,
    "issue_number" integer NOT NULL,
    "journal_title" varchar(250) NOT NULL
)
;
CREATE TABLE "journal_page" (
    "page_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "page" ("id") DEFERRABLE INITIALLY DEFERRED,
    "journal_issue_id" integer NOT NULL REFERENCES "journal_issue" ("dataitem2_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "section_header" varchar(250) NOT NULL
)
;
CREATE TABLE "journal_article" (
    "article_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "article" ("id") DEFERRABLE INITIALLY DEFERRED,
    "journal_issue_id" integer NOT NULL REFERENCES "journal_issue" ("dataitem2_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "citation_full_title" varchar(250) NOT NULL,
    "citation_display_title" varchar(250) NOT NULL,
    "citation_author" varchar(250) NOT NULL
)
;
CREATE TABLE "category" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(250) NOT NULL UNIQUE
)
;
CREATE TABLE "newspaper_issue" (
    "dataitem_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "pub_date" date NOT NULL,
    "page_width" integer NOT NULL,
    "page_height" integer NOT NULL
)
;
CREATE TABLE "newspaper_page" (
    "page_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "page" ("id") DEFERRABLE INITIALLY DEFERRED,
    "newspaper_issue_id" integer NOT NULL REFERENCES "newspaper_issue" ("dataitem_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "supplement_title" varchar(150) NOT NULL
)
;
CREATE TABLE "newspaper_article" (
    "article_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "article" ("id") DEFERRABLE INITIALLY DEFERRED,
    "newspaper_issue_id" integer NOT NULL REFERENCES "newspaper_issue" ("dataitem_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(250) NOT NULL,
    "subtitle" varchar(250) NOT NULL,
    "author" varchar(250) NOT NULL,
    "alt_source" varchar(250) NOT NULL,
    "category_id" integer NOT NULL REFERENCES "category" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "asset" (
    "id" serial NOT NULL PRIMARY KEY,
    "item_id" integer NOT NULL REFERENCES "item" ("id") DEFERRABLE INITIALLY DEFERRED,
    "provider" varchar(64) NOT NULL
)
;
CREATE TABLE "audio_asset" (
    "asset_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "asset" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "image_asset" (
    "asset_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "asset" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "mp3_asset" (
    "audioasset_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "audio_asset" ("asset_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(250) NOT NULL UNIQUE
)
;
CREATE TABLE "wav_asset" (
    "audioasset_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "audio_asset" ("asset_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(250) NOT NULL UNIQUE
)
;
CREATE TABLE "flac_asset" (
    "audioasset_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "audio_asset" ("asset_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(250) NOT NULL UNIQUE
)
;
CREATE TABLE "xml_asset" (
    "asset_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "asset" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(250) NOT NULL UNIQUE
)
;
CREATE TABLE "jpg_asset" (
    "imageasset_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "image_asset" ("asset_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(250) NOT NULL UNIQUE
)
;
CREATE TABLE "tiff_asset" (
    "imageasset_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "image_asset" ("asset_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(250) NOT NULL UNIQUE
)
;
CREATE INDEX "item_status" ON "item" ("status");
CREATE INDEX "item2_pub_date_start" ON "item2" ("pub_date_start");
CREATE INDEX "item2_pub_date_end" ON "item2" ("pub_date_end");
CREATE INDEX "page_item_id" ON "page" ("item_id");
CREATE INDEX "clip_page_id" ON "clip" ("page_id");
CREATE INDEX "article_item_id" ON "article" ("item_id");
CREATE INDEX "qa_illustration_clip_id" ON "qa_illustration" ("clip_id");
CREATE INDEX "journal_page_journal_issue_id" ON "journal_page" ("journal_issue_id");
CREATE INDEX "journal_article_journal_issue_id" ON "journal_article" ("journal_issue_id");
CREATE INDEX "newspaper_issue_pub_date" ON "newspaper_issue" ("pub_date");
CREATE INDEX "newspaper_page_newspaper_issue_id" ON "newspaper_page" ("newspaper_issue_id");
CREATE INDEX "newspaper_article_newspaper_issue_id" ON "newspaper_article" ("newspaper_issue_id");
CREATE INDEX "newspaper_article_category_id" ON "newspaper_article" ("category_id");
CREATE INDEX "asset_item_id" ON "asset" ("item_id");
COMMIT;

