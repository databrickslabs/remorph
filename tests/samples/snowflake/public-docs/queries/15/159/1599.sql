-- see https://docs.snowflake.com/en/sql-reference/functions/decode

SELECT column1, decode(column1, 
                       1, 'one', 
                       2, 'two', 
                       NULL, '-NULL-'
                       ) AS decode_result
    FROM d;