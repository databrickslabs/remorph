
-- source:
DELETE FROM Table1 USING table2 WHERE table1.id = table2.id;

-- databricks_sql:
MERGE INTO  TABLE1 using table2 on table1.id = table2.id when matched then delete;
