-- see https://docs.snowflake.com/en/sql-reference/functions/current_available_roles

SELECT INDEX,VALUE,THIS FROM TABLE(FLATTEN(input => PARSE_JSON(CURRENT_AVAILABLE_ROLES())));
