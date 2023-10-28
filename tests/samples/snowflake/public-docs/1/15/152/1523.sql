select *
from table(information_schema.stage_storage_usage_history(dateadd('days',-10,current_date()),current_date()));