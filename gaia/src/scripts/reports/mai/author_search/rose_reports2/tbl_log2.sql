create table tbl_log2 (
feed_file varchar,
document_instance varchar,
psmid varchar,
articleid varchar,
assetid varchar,
title varchar,
authors varchar
);

CREATE INDEX tbl_log_psmid_assetid_idx2
  ON tbl_log2
  USING btree
  (psmid COLLATE pg_catalog."default", assetid COLLATE pg_catalog."default");

CREATE INDEX tbl_log_psmid_idx2
  ON tbl_log2
  USING btree
  (psmid COLLATE pg_catalog."default");
