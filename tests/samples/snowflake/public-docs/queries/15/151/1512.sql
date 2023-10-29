-- see https://docs.snowflake.com/en/sql-reference/functions/to_binary

SELECT TO_VARCHAR(TO_BINARY('SNOW', 'utf-8'), 'HEX');