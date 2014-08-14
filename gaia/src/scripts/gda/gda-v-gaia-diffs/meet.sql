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
  (feed_file.fname = 'PSM-CHOA_20131028_00600.xml.gz')
  ) AS A
order by dom_name asc
