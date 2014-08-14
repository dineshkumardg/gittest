SELECT 
  tbl_log.psmid, 
  tbl_log.title, 
  tbl_mercury_ids.asset_id, 
  tbl_mercury_ids.mercury_article_id
FROM 
  public.tbl_log, 
  public.tbl_mercury_ids
WHERE 
  tbl_log.assetid = tbl_mercury_ids.asset_id
ORDER BY
  tbl_log.psmid ASC;
