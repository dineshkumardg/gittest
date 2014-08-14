select distinct * 
FROM 
(SELECT 
  item.dom_name
FROM 
  public.feed_file, 
  public.feed_file_items,
  public.item
WHERE 
  feed_file_items.feedfile_id = feed_file.id AND
  item.id = feed_file_items.item_id AND
  (feed_file.fname = 'NOINDEX-CHOA_20130924_00485.xml.gz')
  ) AS A
order by dom_name asc
