-- see https://docs.snowflake.com/en/sql-reference/functions/system_get_tag

select system$get_tag('fiscal_quarter', 'my_table.revenue', 'column');
