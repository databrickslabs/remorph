-- see https://docs.snowflake.com/en/sql-reference/sql/create-table

CREATE TABLE testtable_summary (name, summary_amount) AS SELECT name, amount1 + amount2 FROM testtable;