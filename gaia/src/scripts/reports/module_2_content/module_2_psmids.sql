SELECT distinct
  item.dom_name
  -- substring(item.dom_name, 1, 8)
FROM 
  public.feed_file, 
  public.feed_file_items, 
  public.item
WHERE 
  feed_file_items.item_id = item.id AND
  feed_file_items.feedfile_id = feed_file.id AND
  feed_file.fname IN ('NOINDEX-CHOA_20140428_00755.xml.gz', 
'NOINDEX-CHOA_20140428_00756.xml.gz', 
'PSM-CHOA_20140428_00757.xml.gz', 
'NOINDEX-CHOA_20140428_00758.xml.gz', 
'NOINDEX-CHOA_20140428_00759.xml.gz', 
'PSM-CHOA_20140428_00760.xml.gz', 
'NOINDEX-CHOA_20140428_00761.xml.gz', 
'NOINDEX-CHOA_20140428_00762.xml.gz', 
'PSM-CHOA_20140428_00763.xml.gz', 
'NOINDEX-CHOA_20140428_00764.xml.gz', 
'NOINDEX-CHOA_20140428_00765.xml.gz', 
'PSM-CHOA_20140428_00766.xml.gz', 
'PSM-CHOA_20140429_00775.xml.gz', 
'NOINDEX-CHOA_20140429_00776.xml.gz', 
'PSM-CHOA_20140428_00767.xml.gz', 
'NOINDEX-CHOA_20140428_00768.xml.gz', 
'PSM-CHOA_20140428_00769.xml.gz', 
'NOINDEX-CHOA_20140428_00770.xml.gz', 
'NOINDEX-CHOA_20140425_00740.xml.gz', 
'NOINDEX-CHOA_20140425_00741.xml.gz', 
'PSM-CHOA_20140425_00742.xml.gz')
ORDER BY dom_name ASC