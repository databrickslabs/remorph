-- see https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_config

select key, value from table(flatten(input=>parse_json(SYSTEM$GET_PRIVATELINK_CONFIG())));
