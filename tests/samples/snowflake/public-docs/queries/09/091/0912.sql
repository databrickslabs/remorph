-- see https://docs.snowflake.com/en/sql-reference/functions/endswith

SELECT * FROM strings;


SELECT * FROM strings WHERE ENDSWITH(s, 'te');
