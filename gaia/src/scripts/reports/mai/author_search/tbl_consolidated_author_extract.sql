create table tbl_consolidated_author_extract (
PSMID varchar,
Fulltitle varchar,
ArticleSequence varchar,
Title varchar,
CHOPubType varchar,
Aucomposed varchar,
Prefix varchar,
First varchar,
Middle varchar,
Last varchar,
Suffix varchar,
AtlasHubUID varchar,
PNANotes varchar
);

CREATE INDEX tbl_consolidated_author_extract_psmid_idx2
  ON tbl_consolidated_author_extract
  USING btree
  (psmid COLLATE pg_catalog."default");
