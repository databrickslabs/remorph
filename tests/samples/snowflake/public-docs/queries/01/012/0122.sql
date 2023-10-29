-- see https://docs.snowflake.com/en/sql-reference/transactions

ALTER SESSION SET LOCK_TIMEOUT=7200;

SHOW PARAMETERS LIKE 'lock%';
