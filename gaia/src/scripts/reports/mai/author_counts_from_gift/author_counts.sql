SELECT count(tbl_log.authors) as count, 'conferences' as content_type
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Confer%'
union  
SELECT count(tbl_log.authors) as count, 'books' as content_type
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Books%'
union  
SELECT count(tbl_log.authors) as count, 'journals' as content_type
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Journals%'
union  
SELECT count(tbl_log.authors) as count, 'wrfp' as content_type
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'WRFP%'
union  
SELECT count(tbl_log.authors) as count, 'survey_and_documents' as content_type
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Survey and Documents%'
union  
SELECT count(tbl_log.authors) as count, 'refugee_survey' as content_type
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Refugee%'
union  
SELECT count(tbl_log.authors) as count, 'pamphlets' as content_type
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Pamphlets%'
union  
SELECT count(tbl_log.authors) as count, 'meetings' as content_type
FROM 
  public.tbl_log
WHERE 
  tbl_log.authors IS NOT NULL AND
  feed_file LIKE 'Meetings%'