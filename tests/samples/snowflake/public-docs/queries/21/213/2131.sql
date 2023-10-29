-- see https://docs.snowflake.com/en/sql-reference/functions/external_table_registration_history

select *
from table(information_schema.external_table_file_registration_history(TABLE_NAME=>'MYTABLE'));