-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_substr

SELECT body, REGEXP_SUBSTR(body, '\\b\\S*o\\S*\\b', 3, 3, 'i') AS result FROM message;
