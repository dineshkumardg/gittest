SELECT 
  tbl_log.psmid, 
  tbl_log.articleid, 
  tbl_log.title, 
  tbl_log.authors, 
  tbl_log.assetid
FROM 
  public.tbl_log
WHERE 
  tbl_log.psmid LIKE 'cho_iprx%' OR
  tbl_log.psmid LIKE 'cho_bcrc%' 
ORDER BY
  tbl_log.psmid ASC, 
  cast(tbl_log.articleid as integer) ASC;
