-- see https://docs.snowflake.com/en/sql-reference/functions/system_whitelist

SELECT t.VALUE:type::VARCHAR as type,
       t.VALUE:host::VARCHAR as host,
       t.VALUE:port as port
FROM TABLE(FLATTEN(input => PARSE_JSON(SYSTEM$WHITELIST()))) AS t;