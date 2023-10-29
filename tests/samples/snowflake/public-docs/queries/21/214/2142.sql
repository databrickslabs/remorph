-- see https://docs.snowflake.com/en/sql-reference/functions/stage_storage_usage_history

select *
from table(information_schema.stage_storage_usage_history(dateadd('days',-10,current_date()),current_date()));