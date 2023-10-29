-- see https://docs.snowflake.com/en/sql-reference/account-usage

select date_trunc(month, usage_date) as usage_month
  , avg(storage_bytes + stage_bytes + failsafe_bytes) / power(1024, 4) as billable_tb
from storage_usage
group by 1
order by 1;