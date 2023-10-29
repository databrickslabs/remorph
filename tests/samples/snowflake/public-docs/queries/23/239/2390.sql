-- see https://docs.snowflake.com/en/sql-reference/account-usage

select user_name,
       avg(execution_time) as average_execution_time
from query_history
where start_time >= date_trunc(month, current_date)
group by 1
order by 2 desc;