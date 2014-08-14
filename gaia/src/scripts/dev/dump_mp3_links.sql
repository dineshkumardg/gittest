-- To dump items which have a related mp3 file:
--
-- on postgres:
--      psql -U gaia -d cho -f dump_mp3_links.sql
--
-- on sqllite:
--      sqlite3 -header -column -nullvalue "NULL" xxx.db < dump_mp3_links.sql
SELECT
    i.id AS "ITEM ID",
    l.dom_id AS "DOM_ID",
    i.dom_name AS "ITEM_DOM_NAME",
    l.dom_name AS "LINK_DOM_NAME", 
    i.date AS "DATE" 
FROM
    item i, link l, document d
WHERE
    l.document_id = d.id AND
    d.item_id     = i.id AND
    l.dom_name LIKE '%.mp3';


