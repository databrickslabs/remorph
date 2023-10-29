-- see https://docs.snowflake.com/en/sql-reference/functions/login_history

select *
from table(information_schema.login_history_by_user())
order by event_timestamp;