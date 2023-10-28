select *
from table(information_schema.query_history_by_session())
order by start_time;