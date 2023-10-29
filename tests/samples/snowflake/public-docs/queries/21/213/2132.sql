-- see https://docs.snowflake.com/en/sql-reference/functions/external_table_files

select *
from table(information_schema.external_table_files(TABLE_NAME=>'MYTABLE'));