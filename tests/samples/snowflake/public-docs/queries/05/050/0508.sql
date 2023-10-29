-- see https://docs.snowflake.com/en/sql-reference/sql/create-table

CREATE TABLE mytable (amount NUMBER);

INSERT INTO mytable VALUES(1);

SELECT * FROM mytable;


CREATE TABLE mytable_2 LIKE mytable;

DESC TABLE mytable_2;


SELECT * FROM mytable_2;
