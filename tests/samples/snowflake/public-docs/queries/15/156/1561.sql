-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_substr

SELECT body, REGEXP_SUBSTR(body, '(H\\S*o\\S*\\b).*', 1, 1, '') AS result FROM message;
