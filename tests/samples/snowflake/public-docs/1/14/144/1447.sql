select *
from table(information_schema.external_table_files(TABLE_NAME=>'MYTABLE'));