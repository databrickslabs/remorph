-- see https://docs.snowflake.com/en/sql-reference/functions-regexp

SELECT REGEXP_SUBSTR('Customers - (NY)','\\([[:alnum:]]+\\)') as customers;
