-- see https://docs.snowflake.com/en/sql-reference/functions/endswith

SELECT ENDSWITH(COLLATE('ñn', 'sp'), COLLATE('n', 'sp'));