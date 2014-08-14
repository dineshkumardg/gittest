-- everything in outbox that not on callisto, some of this is fine
select 
	tbl_gaia_outbox.psmid
from 
	tbl_gaia_outbox 
left outer join 
	tbl_callisto 
on 
	tbl_gaia_outbox.psmid = tbl_callisto.psmid
where
    tbl_callisto.psmid is null and
    tbl_gaia_outbox.psmid not like '%TESTLESS%' and 
    tbl_gaia_outbox.psmid not like 'cho_iaxx_2010_7771%' and
    tbl_gaia_outbox.psmid not like 'cho_meet_2010_7771%' and
    tbl_gaia_outbox.psmid not like '%TESTUBE%' and
    tbl_gaia_outbox.psmid not like 'cho_bcrc_1954_0000_000_% %' and 
    tbl_gaia_outbox.psmid not like 'cho__c%' and
    
    left(tbl_gaia_outbox.psmid, 24) not in (
	SELECT 
		distinct left(psmid, 24) as psmid
	FROM 
		tbl_gaia_released
    )

order by 
	psmid asc;