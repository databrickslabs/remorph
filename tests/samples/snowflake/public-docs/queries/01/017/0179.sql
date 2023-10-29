-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table-column

ALTER TABLE t1 ALTER (
   c1 DROP NOT NULL,
   c5 COMMENT '50 character column',
   c4 TYPE VARCHAR(50),
   c2 DROP DEFAULT,
   COLUMN c4 DROP DEFAULT,
   COLUMN c3 SET DEFAULT seq5.nextval
  );