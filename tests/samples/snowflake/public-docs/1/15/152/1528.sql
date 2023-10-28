use warehouse mywarehouse;

select *
from table(information_schema.warehouse_load_history(date_range_start=>dateadd('hour',-1,current_timestamp())));