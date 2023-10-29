-- see https://docs.snowflake.com/en/sql-reference/functions/replication_group_refresh_progress

select *
from table(information_schema.replication_group_refresh_progress_by_job('012a3b45-1234-a12b-0000-1aa200012345'));