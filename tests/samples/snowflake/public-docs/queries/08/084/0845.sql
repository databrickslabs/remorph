-- see https://docs.snowflake.com/en/sql-reference/functions/split_to_table

SELECT * 
    FROM splittable, LATERAL SPLIT_TO_TABLE(splittable.v, '.')
    ORDER BY SEQ, INDEX;