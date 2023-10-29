-- see https://docs.snowflake.com/en/sql-reference/functions/reverse

SELECT s1, s2, REVERSE(s1), REVERSE(s2) 
    FROM strings;