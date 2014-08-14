SELECT 
  tbl_consolidated_author_extract.psmid AS htc_psmid, 
  tbl_consolidated_author_extract.articlesequence AS htc_article_id, 
  tbl_consolidated_author_extract.aucomposed AS htc_author, 
  tbl_log.authors AS gift_author, 
  tbl_log.assetid AS gift_asset_id, 
  tbl_consolidated_author_extract.atlashubuid AS atlas_uid
FROM 
  public.tbl_consolidated_author_extract, 
  public.tbl_log
WHERE 
  tbl_consolidated_author_extract.psmid = tbl_log.psmid AND
  tbl_consolidated_author_extract.articlesequence = tbl_log.articleid AND
  tbl_consolidated_author_extract.psmid LIKE 'cho_book%' AND 
  tbl_consolidated_author_extract.aucomposed IS NOT NULL
ORDER BY
  tbl_consolidated_author_extract.psmid ASC;
