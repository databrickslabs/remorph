-- see https://docs.snowflake.com/en/sql-reference/sql/merge

MERGE INTO target_table USING source_table 
    ON target_table.id = source_table.id
    WHEN MATCHED THEN 
        UPDATE SET target_table.description = source_table.description;