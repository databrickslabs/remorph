-- see https://docs.snowflake.com/en/sql-reference/functions/system_get_tag

select system$get_tag('cost_center', 'my_table', 'table');
