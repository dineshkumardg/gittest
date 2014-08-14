SELECT 
  distinct left(tbl_gaia_released.psmid, 24) as psmid
FROM 
  tbl_gaia_released
left outer join
  tbl_callisto
on  
  left(tbl_gaia_released.psmid, 24) = left(tbl_callisto.psmid, 24)
where
  tbl_callisto.psmid is null
 order by psmid asc 