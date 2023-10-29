-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table-event-table

ALTER TABLE t1
  ADD ROW ACCESS POLICY rap_test2 ON (cost, item);