-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table-event-table

alter table t1
  drop row access policy rap_t1_version_1,
  add row access policy rap_t1_version_2 on (empl_id);