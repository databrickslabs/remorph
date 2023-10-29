-- see https://docs.snowflake.com/en/sql-reference/functions/try_parse_json

SELECT ID, try_parse_json(v) 
    FROM vartab
    ORDER BY ID;