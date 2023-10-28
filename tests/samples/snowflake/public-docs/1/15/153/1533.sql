select *
from table(information_schema.query_history(dateadd('hours',-1,current_timestamp()),current_timestamp()))
order by start_time;