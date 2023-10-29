-- see https://docs.snowflake.com/en/sql-reference/sql/merge

MERGE INTO t1 USING t2 ON t1.t1Key = t2.t2Key
    WHEN MATCHED AND t2.marked = 1 THEN DELETE
    WHEN MATCHED AND t2.isNewStatus = 1 THEN UPDATE SET val = t2.newVal, status = t2.newStatus
    WHEN MATCHED THEN UPDATE SET val = t2.newVal
    WHEN NOT MATCHED THEN INSERT (val, status) VALUES (t2.newVal, t2.newStatus);