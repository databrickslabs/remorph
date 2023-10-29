-- see https://docs.snowflake.com/en/sql-reference/functions/query_history

select *
from table(information_schema.query_history_by_session())
order by start_time;