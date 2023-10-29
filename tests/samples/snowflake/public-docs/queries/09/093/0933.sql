-- see https://docs.snowflake.com/en/sql-reference/functions/contains

SELECT * from strings;


SELECT * FROM strings WHERE CONTAINS(s, 'te');
