
-- snowflake sql:
UPDATE t1
                            SET column1 = t1.column1 + t2.column1, column3 = 'success'
                            FROM t2
                            WHERE t1.key = t2.t1_key and t1.column1 < 10;

-- databricks sql:
MERGE INTO t1 USING t2 ON t1.key = t2.t1_key and t1.column1 < 10 WHEN MATCHED THEN UPDATE SET column1 = t1.column1 + t2.column1,
column3 = 'success';
