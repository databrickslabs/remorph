-- see https://docs.snowflake.com/en/sql-reference/sql/alter-external-table

BEGIN;

ALTER EXTERNAL TABLE extable1 REMOVE FILES ('2019/12/log1.json.gz');

ALTER EXTERNAL TABLE extable1 ADD FILES ('2019/12/log1.json.gz');

COMMIT;