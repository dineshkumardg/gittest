-- levelled-log_log2 = shows where there are more articles sequnces changes
SELECT 
  tbl_log.psmid, 
  tbl_log.articleid as early_articlid, 
  tbl_log2.articleid as latest_articleid
FROM 
  public.tbl_log, 
  public.tbl_log2
WHERE 
  tbl_log.psmid = tbl_log2.psmid AND
  tbl_log.articleid <> tbl_log2.articleid AND
  tbl_log.assetid = tbl_log2.assetid
ORDER BY
  tbl_log.psmid ASC, tbl_log.articleid ASC;