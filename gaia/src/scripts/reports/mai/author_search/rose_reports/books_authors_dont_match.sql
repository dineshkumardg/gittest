SELECT 
  tbl_log.psmid AS gift_psmid, 
  tbl_log.articleid AS gift_article_id, 
  tbl_log.authors AS gift_author, 
  tbl_consolidated_author_extract.aucomposed AS htc_author
FROM 
  public.tbl_log, 
  public.tbl_consolidated_author_extract
WHERE 
  tbl_log.psmid = tbl_consolidated_author_extract.psmid AND
  tbl_log.articleid = tbl_consolidated_author_extract.articlesequence AND
  tbl_log.authors != tbl_consolidated_author_extract.aucomposed AND 
  tbl_log.psmid LIKE 'cho_book%'
ORDER BY
  tbl_log.psmid ASC, 
  tbl_log.articleid ASC;
