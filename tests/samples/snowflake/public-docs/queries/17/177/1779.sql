-- see https://docs.snowflake.com/en/sql-reference/functions/strtok_split_to_table

SELECT table1.value 
    FROM table(strtok_split_to_table('a.b', '.')) AS table1
    ORDER BY table1.value;