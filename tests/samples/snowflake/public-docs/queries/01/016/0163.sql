-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table

ALTER TABLE exttable1 ADD COLUMN a1 VARCHAR AS (value:a1::VARCHAR);