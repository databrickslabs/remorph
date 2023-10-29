-- see https://docs.snowflake.com/en/sql-reference/functions/system_get_tag_allowed_values

select system$get_tag_allowed_values('governance.tags.cost_center');