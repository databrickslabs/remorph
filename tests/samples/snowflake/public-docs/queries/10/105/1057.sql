-- see https://docs.snowflake.com/en/sql-reference/functions/trim

SELECT CONCAT('>', CONCAT(v, '<')), CONCAT('>', CONCAT(TRIM(v), '<')) FROM tr;
