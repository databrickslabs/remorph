-- see https://docs.snowflake.com/en/sql-reference/functions/strtok_split_to_table

SELECT * 
    FROM splittable, LATERAL STRTOK_SPLIT_TO_TABLE(splittable.v, ' |')
    ORDER BY SEQ, INDEX;