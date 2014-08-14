--
-- The way gaia was designed (by Tushar Wagle) is very object orientated - what this means is that the postgres database needs
-- some indexes on  common.order_by( and .filter. Even so, some of the queries are still very slow. The lesson being that you
-- should design the database base first and then the objects?
--
-- ideally the model would use: db_index=True,
-- i.e.
-- class Blog(models.Model):
--     title = models.CharField(db_index=True, max_length=100)
--     added = models.DateTimeField(db_index=True, auto_now_add=True)
--     body = models.TextField()
--
-- RE: https://docs.djangoproject.com/en/1.4/topics/db/optimization/:q!
--

BEGIN;

DROP INDEX IF EXISTS m_code_psmid_mcode_publication_title;
CREATE INDEX m_code_psmid_mcode_publication_title
   ON m_codes
   USING btree
   (mcode ASC NULLS LAST, psmid ASC NULLS LAST, publication_title ASC NULLS LAST);

DROP INDEX IF EXISTS item_id;
CREATE INDEX item_id
  ON item
  USING btree
  (id DESC NULLS FIRST);

DROP INDEX IF EXISTS item_date;
CREATE INDEX item_date
   ON item
   USING btree
   (date DESC NULLS FIRST);

DROP INDEX IF EXISTS feed_file_when;
CREATE INDEX feed_file_when
   ON feed_file
   USING btree
   ("when" DESC NULLS FIRST);

DROP INDEX IF EXISTS page_final_id_page;
CREATE INDEX page_final_id_page
   ON page_final_id
   USING btree
   (page_id ASC NULLS LAST);

DROP INDEX IF EXISTS chunk_final_id_chunk;
CREATE INDEX chunk_final_id_chunk
   ON chunk_final_id
   USING btree
   (chunk_id ASC NULLS LAST);

DROP INDEX IF EXISTS ingest_error_when;
CREATE INDEX ingest_error_when
   ON ingest_error
   USING btree
   ("when" DESC NULLS FIRST);

DROP INDEX IF EXISTS item_error_when;
CREATE INDEX item_error_when
   ON item_errors
   USING btree
   ("when" DESC NULLS FIRST);

DROP INDEX IF EXISTS item_dom_id;
CREATE INDEX item_dom_id
   ON item USING btree (dom_id ASC NULLS LAST);

DROP INDEX IF EXISTS item_dom_id_dom_name;
CREATE INDEX item_dom_id_dom_name
   ON item USING btree (dom_id ASC NULLS LAST, dom_name ASC NULLS LAST);

DROP INDEX IF EXISTS chunk_dom_id;
CREATE INDEX chunk_dom_id
   ON chunk USING btree (dom_id ASC NULLS LAST);

DROP INDEX IF EXISTS page_dom_id;
CREATE INDEX page_dom_id
  ON page
  USING btree
  (dom_id ASC NULLS LAST);

DROP INDEX IF EXISTS item_dom_id_dom_name_is_live;
CREATE INDEX item_dom_id_dom_name_is_live
   ON item USING btree (dom_id ASC NULLS LAST, dom_name ASC NULLS LAST, is_live ASC NULLS LAST);

DROP INDEX IF EXISTS item_is_live_dom_name;
CREATE INDEX item_is_live_dom_name
   ON item USING btree (is_live ASC NULLS LAST, dom_name ASC NULLS LAST);

DROP INDEX IF EXISTS m_codes_psmid;
CREATE INDEX m_codes_psmid
   ON m_codes USING btree (psmid ASC NULLS LAST);

DROP INDEX IF EXISTS chunk_document_id_is_binary;
CREATE INDEX chunk_document_id_is_binary
   ON chunk USING btree (document_id ASC NULLS LAST, is_binary ASC NULLS LAST);

DROP INDEX IF EXISTS document_final_id_final_id;
CREATE INDEX document_final_id_final_id
   ON document_final_id USING btree (final_id ASC NULLS LAST);

DROP INDEX IF EXISTS page_final_id_final_id;
CREATE INDEX page_final_id_final_id
   ON page_final_id USING btree (final_id ASC NULLS LAST);

DROP INDEX IF EXISTS feed_file_fname;
CREATE INDEX feed_file_fname
   ON feed_file USING btree (fname ASC NULLS LAST);

DROP INDEX IF EXISTS asset_link__link_ptr_id;
CREATE INDEX asset_link__link_ptr_id
   ON asset_link USING btree (_link_ptr_id ASC NULLS LAST);

DROP INDEX IF EXISTS link_id;
CREATE INDEX link_id
   ON link USING btree (id ASC NULLS LAST);

COMMIT;