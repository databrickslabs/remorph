WITH RECURSIVE current_layer (indent, layer_ID, parent_component_ID, component_id, description, sort_key) AS (
  SELECT 
      '...', 
      1, 
      parent_component_ID, 
      component_id, 
      description, 
      '0001'
    FROM components WHERE component_id = 1
  UNION ALL
  SELECT indent || '...',
      layer_ID + 1,
      components.parent_component_ID,
      components.component_id, 
      components.description,
      sort_key || SUBSTRING('000' || components.component_ID, -4)
    FROM current_layer JOIN components 
      ON (components.parent_component_id = current_layer.component_id)
  )
SELECT
  -- The indentation gives us a sort of "side-ways tree" view, with
  -- sub-components indented under their respective components.
  indent || description AS description, 
  component_id,
  parent_component_ID
  -- The layer_ID and sort_key are useful for debugging, but not
  -- needed in the report.
--  , layer_ID, sort_key
  FROM current_layer
  ORDER BY sort_key;