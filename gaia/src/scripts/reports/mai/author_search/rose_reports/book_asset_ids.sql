SELECT 
  tbl_log.psmid as psmid, 
  tbl_log.articleid as articleid, 
  tbl_log.title as gift_title, 
  tbl_log.authors as gift_authors, 
  tbl_consolidated_author_extract.aucomposed as htc_authors,
  tbl_log.assetid as gift_asset_id, 
  tbl_consolidated_author_extract.atlashubuid as atlas_uid
FROM 
  public.tbl_log
LEFT OUTER JOIN tbl_consolidated_author_extract
ON tbl_log.psmid=tbl_consolidated_author_extract.psmid
WHERE 
  tbl_log.psmid LIKE 'cho_book%'
ORDER BY
  tbl_log.psmid ASC, 
  tbl_log.document_instance ASC 
