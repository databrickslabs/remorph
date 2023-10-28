select *
from table(information_schema.login_history(TIME_RANGE_START => dateadd('hours',-1,current_timestamp()),current_timestamp()))
order by event_timestamp;