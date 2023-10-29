-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table-event-table

ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2);
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c3, c4);