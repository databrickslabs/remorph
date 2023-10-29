-- see https://docs.snowflake.com/en/sql-reference/functions/get_ddl

select get_ddl('function', 'multiply(number, number)');
