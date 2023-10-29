-- see https://docs.snowflake.com/en/sql-reference/sql/create-table

CREATE TABLE mytable_copy (b) AS SELECT * FROM mytable;

DESC TABLE mytable_copy;


CREATE TABLE mytable_copy2 AS SELECT b+1 AS c FROM mytable_copy;

DESC TABLE mytable_copy2;


SELECT * FROM mytable_copy2;
