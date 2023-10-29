-- see https://docs.snowflake.com/en/sql-reference/functions/split_to_table

SELECT table1.value 
    FROM table(split_to_table('a.b', '.')) AS table1
    ORDER BY table1.value;