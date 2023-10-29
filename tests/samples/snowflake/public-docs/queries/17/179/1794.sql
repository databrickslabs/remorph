-- see https://docs.snowflake.com/en/sql-reference/functions/lpad

SELECT v, LPAD(v, 10, ' '),             
          LPAD(v, 10, '$')
    FROM demo
    ORDER BY v;