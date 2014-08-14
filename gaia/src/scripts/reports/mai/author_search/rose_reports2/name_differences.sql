
SELECT 
  tbl_log.psmid, 
  tbl_log.articleid as early_articlesequence,
  tbl_log2.articleid as latest_articlesequence,
  tbl_log.title as early_fulltitle,
  tbl_log2.title as latest_fulltitle,
  tbl_log.authors as early_aucomposed,
  tbl_log2.authors as latest_aucomposed,
  tbl_log.assetid as early_assetid,
  tbl_log2.assetid as latest_assetid,
  '' as atlashubuid
FROM 
  public.tbl_log, 
  public.tbl_log2
WHERE 
  tbl_log.psmid = tbl_log2.psmid AND
  tbl_log.articleid = tbl_log2.articleid AND
  tbl_log.title <> tbl_log2.title AND 
  (tbl_log.authors <> '' OR tbl_log2.authors <> '' OR tbl_log2.authors is null)
ORDER BY 
  tbl_log.psmid ASC, tbl_log.articleid::int ASC;
