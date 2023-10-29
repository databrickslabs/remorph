-- see https://docs.snowflake.com/en/sql-reference/functions/database_storage_usage_history

select *
from table(information_schema.database_storage_usage_history(dateadd('days',-10,current_date()),current_date()));