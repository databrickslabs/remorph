-- see https://docs.snowflake.com/en/sql-reference/literals-table

SET myvar = 'mytable';

SELECT * FROM TABLE($myvar);