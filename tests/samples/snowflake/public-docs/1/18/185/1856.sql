select key, value from table(flatten(input=>parse_json(SYSTEM$GET_PRIVATELINK_CONFIG())));
