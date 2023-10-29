-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table

alter table t1 add row access policy rap_t1 on (empl_id);