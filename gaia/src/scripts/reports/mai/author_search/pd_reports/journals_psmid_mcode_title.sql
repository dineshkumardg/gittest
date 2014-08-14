SELECT 
  tbl_log.psmid, 
  rmt_view_m_codes.mcode, 
  tbl_log.title
FROM 
  public.tbl_log, 
  public.rmt_view_m_codes
WHERE 
  tbl_log.psmid = rmt_view_m_codes.psmid AND
  tbl_log.psmid LIKE 'cho_binx%' OR 
  tbl_log.psmid LIKE 'cho_iaxx%' OR 
  tbl_log.psmid LIKE 'cho_wtxx%'
ORDER BY
  tbl_log.psmid ASC, 
  rmt_view_m_codes.mcode ASC;
