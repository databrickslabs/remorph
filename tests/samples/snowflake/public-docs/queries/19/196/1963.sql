-- see https://docs.snowflake.com/en/sql-reference/sql/alter-view

alter view v1
  add row access policy rap_v1 on (empl_id);