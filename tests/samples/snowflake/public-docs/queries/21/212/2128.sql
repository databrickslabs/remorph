-- see https://docs.snowflake.com/en/sql-reference/functions/database_refresh_progress

select *
from table(information_schema.database_refresh_progress(mydb1));