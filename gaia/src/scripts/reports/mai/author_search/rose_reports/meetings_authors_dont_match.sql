SELECT distinct
  tbl_log.psmid as psmid, 
  cast(tbl_log.articleid as integer) as articleid, 
  tbl_log.title as gift_title,  
  tbl_log.authors as gift_authors, 
  tbl_consolidated_author_extract.aucomposed as htc_authors, 
  tbl_log.assetid as gift_asset_id, 
  tbl_consolidated_author_extract.atlashubuid as atlas_uid
FROM 
  public.tbl_log, 
  public.tbl_consolidated_author_extract
WHERE 
  tbl_log.psmid = tbl_consolidated_author_extract.psmid AND
  tbl_log.psmid like 'cho_meet%' AND
  tbl_log.articleid = tbl_consolidated_author_extract.articlesequence AND
  tbl_log.authors <> tbl_consolidated_author_extract.aucomposed
ORDER BY
  tbl_log.psmid ASC, 
  cast(tbl_log.articleid as integer) ASC;