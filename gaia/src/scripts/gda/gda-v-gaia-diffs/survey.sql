select distinct * 
FROM 
(SELECT 
  distinct item.dom_name
FROM 
  public.feed_file, 
  public.feed_file_items,
  public.item
WHERE 
  feed_file_items.feedfile_id = feed_file.id AND
  item.id = feed_file_items.item_id AND
  (feed_file.fname = 'NOINDEX-CHOA_20131029_00629.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00630.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00626.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00627.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00629.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00630.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00623.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00624.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00626.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00627.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00629.xml.gz' OR
   feed_file.fname = 'NOINDEX-CHOA_20131029_00630.xml.gz')
  ) AS A
order by dom_name asc










