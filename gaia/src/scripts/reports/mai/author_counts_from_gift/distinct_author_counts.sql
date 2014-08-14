SELECT count(a.*) as distinct_count, 'conferences' as content_type
FROM (
SELECT DISTINCT tbl_log.authors
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Confer%'
) a  
  
union  
SELECT count(a.*) as distinct_count, 'books' as content_type
FROM (
SELECT DISTINCT tbl_log.authors
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Books%'
) a  
  
union 
SELECT count(a.*) as distinct_count, 'journals' as content_type  
FROM (
SELECT DISTINCT tbl_log.authors
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Journals%'
) a  
  
union  
SELECT count(a.*) as distinct_count, 'wfrp' as content_type  
FROM ( 
SELECT DISTINCT tbl_log.authors
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'WRFP%'
) a  
  
union  
SELECT count(a.*) as distinct_count, 'survey_and_documents' as content_type  
FROM ( 
SELECT DISTINCT tbl_log.authors
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Survey and Documents%'
) a  
  
union 
SELECT count(a.*) as distinct_count, 'refugee_survey' as content_type    
FROM (
SELECT DISTINCT tbl_log.authors
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Refugee%'
) a  
  
union   
SELECT count(a.*) as distinct_count, 'pamphlets' as content_type  
FROM (
SELECT DISTINCT tbl_log.authors
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Pamphlets%'
) a  
  
union   
SELECT count(a.*) as distinct_count, 'meetings' as content_type  
FROM (
SELECT DISTINCT tbl_log.authors
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Meetings%'
) a  