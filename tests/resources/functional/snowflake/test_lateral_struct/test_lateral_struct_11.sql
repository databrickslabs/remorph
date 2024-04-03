
-- source:
SELECT level_1_key:level_2_key:'1' FROM demo1;

-- databricks_sql:
SELECT level_1_key.level_2_key['1'] FROM demo1;
