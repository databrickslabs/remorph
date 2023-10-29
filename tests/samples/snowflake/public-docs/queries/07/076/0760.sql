-- see https://docs.snowflake.com/en/sql-reference/constructs/connect-by

SELECT
  description,
  quantity,
  component_id, 
  parent_component_ID,
  SYS_CONNECT_BY_PATH(component_ID, ' -> ') AS path
  FROM components
    START WITH component_ID = 1
    CONNECT BY 
      parent_component_ID = PRIOR component_ID
  ORDER BY path
  ;