select *
from table(information_schema.warehouse_metering_history(dateadd('days',-10,current_date())));