
-- source:
SELECT date_part('seconds', col1) AS date_part_col1 FROM tabl;

-- databricks_sql:
SELECT EXTRACT(second FROM col1) AS date_part_col1 FROM tabl;
