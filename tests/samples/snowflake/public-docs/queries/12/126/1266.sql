-- see https://docs.snowflake.com/en/sql-reference/functions/object_construct

SELECT OBJECT_CONSTRUCT(
    'foo', 1234567,
    'dataset_size', (SELECT COUNT(*) FROM demo_table_1),
    'distinct_province', (SELECT COUNT(DISTINCT province) FROM demo_table_1),
    'created_date_seconds', extract(epoch_seconds, created_date)
    )
    FROM demo_table_1;