--
-- The postgres server requires the following sequences are created; this is not required for sqlite
--
-- psql -U postgres -d cho -f ~/GIT_REPOS/gaia/src/scripts/db/cho/create_sequences.sql
--

BEGIN;
CREATE SEQUENCE chunk_document_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE chunk_document_id_seq OWNER TO system_test; 
ALTER SEQUENCE chunk_document_id_seq OWNED BY chunk.document_id;

CREATE SEQUENCE chunk_pages_chunk_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE chunk_pages_chunk_id_seq OWNER TO system_test;
ALTER SEQUENCE chunk_pages_chunk_id_seq OWNED BY chunk_pages.chunk_id;

CREATE SEQUENCE chunk_pages_page_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE chunk_pages_page_id_seq OWNER TO system_test;
ALTER SEQUENCE chunk_pages_page_id_seq OWNED BY chunk_pages.page_id;

CREATE SEQUENCE chunk_qa_activity_chunk_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE chunk_qa_activity_chunk_id_seq OWNER TO system_test;
ALTER SEQUENCE chunk_qa_activity_chunk_id_seq OWNED BY chunk_qa_activity.chunk_id;

CREATE SEQUENCE clip_page_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE clip_page_id_seq OWNER TO system_test;
ALTER SEQUENCE clip_page_id_seq OWNED BY clip.page_id;

CREATE SEQUENCE document_item_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE document_item_id_seq OWNER TO system_test;
ALTER SEQUENCE document_item_id_seq OWNED BY document.item_id;

CREATE SEQUENCE item_errors_item_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE item_errors_item_id_seq OWNER TO system_test;
ALTER SEQUENCE item_errors_item_id_seq OWNED BY item_errors.item_id;

CREATE SEQUENCE item_qa_activity_item_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE item_qa_activity_item_id_seq OWNER TO system_test;
ALTER SEQUENCE item_qa_activity_item_id_seq OWNED BY item_qa_activity.item_id;

CREATE SEQUENCE item_status_item_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE item_status_item_id_seq OWNER TO system_test;
ALTER SEQUENCE item_status_item_id_seq OWNED BY item_status.item_id;

CREATE SEQUENCE link_document_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE link_document_id_seq OWNER TO system_test;
ALTER SEQUENCE link_document_id_seq OWNED BY link.document_id;

CREATE SEQUENCE page_document_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE page_document_id_seq OWNER TO system_test;
ALTER SEQUENCE page_document_id_seq OWNED BY page.document_id;

CREATE SEQUENCE page_qa_activity_page_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE page_qa_activity_page_id_seq OWNER TO system_test;
ALTER SEQUENCE page_qa_activity_page_id_seq OWNED BY page_qa_activity.page_id;

CREATE SEQUENCE asset_link_final_id_link_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE asset_link_final_id_link_id_seq OWNER TO system_test; 
ALTER SEQUENCE asset_link_final_id_link_id_seq OWNED BY asset_link._link_ptr_id;

CREATE SEQUENCE document_link_final_id_link_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE document_link_final_id_link_id_seq OWNER TO system_test; 
ALTER SEQUENCE document_link_final_id_link_id_seq OWNED BY document_link._link_ptr_id;
COMMIT;
