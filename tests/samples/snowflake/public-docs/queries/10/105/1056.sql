-- see https://docs.snowflake.com/en/sql-reference/functions/ltrim

SELECT CONCAT('>', CONCAT(v, '<')), CONCAT('>', CONCAT(LTRIM(v), '<')) FROM tr;
