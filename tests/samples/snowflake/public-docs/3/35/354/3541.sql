set schema_name = 'my_db.my_schema';

set table_name = 'my_table';

use schema identifier($schema_name);

insert into identifier($table_name) values (1), (2), (3);

select * from identifier($table_name) order by 1;
