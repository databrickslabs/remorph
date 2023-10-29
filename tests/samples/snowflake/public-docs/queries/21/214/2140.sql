-- see https://docs.snowflake.com/en/sql-reference/functions/replication_group_refresh_progress

select *
from table(information_schema.replication_group_refresh_progress('rg1'));