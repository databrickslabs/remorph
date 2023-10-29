-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_like

SELECT * FROM cities WHERE REGEXP_LIKE(city, 'san.*');