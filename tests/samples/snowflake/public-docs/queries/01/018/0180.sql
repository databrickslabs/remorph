-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table-column

ALTER TABLE t1 ALTER COLUMN c1 DROP NOT NULL;

ALTER TABLE t1 MODIFY c2 DROP DEFAULT, c3 SET DEFAULT seq5.nextval ;

ALTER TABLE t1 ALTER c4 SET DATA TYPE VARCHAR(50), COLUMN c4 DROP DEFAULT;

ALTER TABLE t1 ALTER c5 COMMENT '50 character column';

DESC TABLE t1;
