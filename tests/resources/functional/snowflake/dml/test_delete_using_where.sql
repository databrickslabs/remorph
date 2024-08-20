-- snowflake sql:
DELETE FROM table1 USING table2 WHERE table1.id = table2.id;

-- databricks sql:
MERGE INTO  table1 USING table2 ON table1.id = table2.id WHEN MATCHED THEN DELETE;
