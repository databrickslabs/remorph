-- see https://docs.snowflake.com/en/sql-reference/functions/rtrim

SELECT CONCAT('>', CONCAT(v, '<')), CONCAT('>', CONCAT(rtrim(v), '<')) FROM tr;
