-- see https://docs.snowflake.com/en/sql-reference/functions/rlike

SELECT * FROM rlike_ex WHERE city RLIKE 'San.* [fF].*';
