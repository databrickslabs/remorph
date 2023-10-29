-- see https://docs.snowflake.com/en/sql-reference/functions/warehouse_load_history

use warehouse mywarehouse;

select *
from table(information_schema.warehouse_load_history(date_range_start=>dateadd('day',-14,current_date()), date_range_end=>current_date()));