-- see https://docs.snowflake.com/en/sql-reference/functions/nvl

SELECT NVL('food', 'bard') AS col1, NVL(NULL, 3.14) AS col2;
