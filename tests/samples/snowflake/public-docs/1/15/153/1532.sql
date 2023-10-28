select *
from table(information_schema.query_history())
order by start_time;