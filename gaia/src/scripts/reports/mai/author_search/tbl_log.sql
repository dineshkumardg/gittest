create table tbl_log4 (
feed_file varchar,
document_instance varchar,
psmid varchar,
articleid varchar,
assetid varchar,
title varchar,
authors varchar
);

CREATE INDEX tbl_log4_psmid_assetid_idx
  ON tbl_log4
  USING btree
  (psmid COLLATE pg_catalog."default", assetid COLLATE pg_catalog."default");

CREATE INDEX tbl_log4_psmid_idx
  ON tbl_log4
  USING btree
  (psmid COLLATE pg_catalog."default");
