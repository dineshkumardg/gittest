SELECT 
  document_final_id.final_id, 
  document.dom_id, 
  chunk.dom_id, 
  chunk_final_id.final_id, 
  chunk.dom_name, 
  item.is_live
FROM 
  public.document_final_id, 
  public.document, 
  public.chunk, 
  public.chunk_final_id, 
  public.item
WHERE 
  document_final_id.document_id = document.id AND
  document.item_id = item.id AND
  chunk.document_id = document.id AND
  chunk_final_id.chunk_id = chunk.id AND
  document.dom_id = 'cho_rpax_1970_royal_009_0000' AND 
  item.is_live = True
ORDER BY
  chunk.dom_name ASC;
