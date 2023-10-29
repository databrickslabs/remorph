-- see https://docs.snowflake.com/en/sql-reference/functions/query_history

select *
from table(information_schema.query_history())
order by start_time;