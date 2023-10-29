-- see https://docs.snowflake.com/en/sql-reference/functions/system_allowlist_privatelink

SELECT t.VALUE:type::VARCHAR as type,
       t.VALUE:host::VARCHAR as host,
       t.VALUE:port as port
FROM TABLE(FLATTEN(input => PARSE_JSON(SYSTEM$ALLOWLIST_PRIVATELINK()))) AS t;