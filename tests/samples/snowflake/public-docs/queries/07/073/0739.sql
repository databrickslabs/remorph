-- see https://docs.snowflake.com/en/sql-reference/functions/case

SELECT
    column1,
    CASE
        WHEN column1=1 THEN 'one'
        WHEN column1=2 THEN 'two'
    END AS result
FROM (values(1),(2),(3)) v;