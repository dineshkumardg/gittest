create table tbl_callisto (
psmid varchar
);

CREATE INDEX tbl_callisto_idx
  ON tbl_callisto
  USING btree
  (psmid COLLATE pg_catalog."default");


create table tbl_gaia_outbox (
psmid varchar
);

CREATE INDEX tbl_gaia_outbox_idx
  ON tbl_gaia_outbox
  USING btree
  (psmid COLLATE pg_catalog."default");


create table tbl_gaia_released (
psmid varchar
);

CREATE INDEX tbl_gaia_released_idx
  ON tbl_gaia_released
  USING btree
  (psmid COLLATE pg_catalog."default");

