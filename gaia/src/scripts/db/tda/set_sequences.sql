-- set the 3 GOLD platform ids:
--  the unique article number (== article.id)
--  the unique page number    (== page.id)
--  the unique issue number   (== item.id)

-- NOTE:
-- CREATE TABLE person (
    -- id SERIAL,
    -- name TEXT
-- );
-- 
-- is automatically translated by postgres into this:
-- 
-- CREATE SEQUENCE person_id_seq;
-- CREATE TABLE person (
    -- id INTEGER NOT NULL DEFAULT nextval('person_id_seq'),
    -- name TEXT
-- );

-- set the Article Id, Page Id and Issue Id to the
-- "zz ranges" as supplied by Farmington Hills.
--  Note: zz numbers are 10-digit values
ALTER SEQUENCE article_id_seq RESTART WITH 0500000000;
ALTER SEQUENCE page_id_seq    RESTART WITH 0600000000;
ALTER SEQUENCE item_id_seq    RESTART WITH 0800000000;
