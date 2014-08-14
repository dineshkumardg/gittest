SELECT 
  psmid, articleid, assetid, count(*) as counter
FROM 
  public.tbl_log4
group by psmid, articleid, assetid
order by counter desc
