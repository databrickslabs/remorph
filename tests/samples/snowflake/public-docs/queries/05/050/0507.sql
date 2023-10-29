-- see https://docs.snowflake.com/en/sql-reference/sql/create-table

CREATE TABLE mytable (amount NUMBER);


INSERT INTO mytable VALUES(1);

SHOW TABLES like 'mytable';


DESC TABLE mytable;
