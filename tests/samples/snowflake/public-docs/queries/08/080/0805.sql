-- see https://docs.snowflake.com/en/sql-reference/functions/in

SELECT 'a' IN (
    SELECT column1 FROM VALUES ('b'), ('c'), ('d')
    ) AS RESULT;