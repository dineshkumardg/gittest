SELECT 
  tbl_consolidated_author_extract.psmid, 
  tbl_consolidated_author_extract.articlesequence, 
  tbl_consolidated_author_extract.fulltitle, 
  tbl_consolidated_author_extract.aucomposed, 
  tbl_consolidated_author_extract.atlashubuid
FROM 
  public.tbl_consolidated_author_extract
WHERE 
  (tbl_consolidated_author_extract.psmid LIKE 'cho_siax%' OR
  tbl_consolidated_author_extract.psmid LIKE 'cho_diax%' OR
  tbl_consolidated_author_extract.psmid LIKE 'cho_sbca%' OR
  tbl_consolidated_author_extract.psmid LIKE 'cho_dsca%' OR
  tbl_consolidated_author_extract.psmid LIKE 'cho_byil%' ) AND
  tbl_consolidated_author_extract.articlesequence <> 'Book Level'
ORDER BY
  tbl_consolidated_author_extract.psmid ASC, 
  cast(tbl_consolidated_author_extract.articlesequence as integer) ASC;
