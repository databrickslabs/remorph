select *
from table(information_schema.external_table_file_registration_history(TABLE_NAME=>'MYTABLE'));