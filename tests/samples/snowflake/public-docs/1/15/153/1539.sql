select *
from table(information_schema.login_history_by_user(USER_NAME => 'USER1', result_limit => 1000))
order by event_timestamp;