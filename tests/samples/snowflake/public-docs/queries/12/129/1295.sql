-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_replace

SELECT REGEXP_REPLACE('Customers - (NY)','\\(|\\)','') AS customers;
