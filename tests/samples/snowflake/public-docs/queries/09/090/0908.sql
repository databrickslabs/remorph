-- see https://docs.snowflake.com/en/sql-reference/functions/rlike

SELECT * FROM rlike_ex WHERE RLIKE(city, 'san.*', 'i');
