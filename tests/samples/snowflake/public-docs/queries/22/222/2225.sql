-- see https://docs.snowflake.com/en/sql-reference/account-usage

select count(*) as number_of_jobs
from query_history
where start_time >= date_trunc(month, current_date);