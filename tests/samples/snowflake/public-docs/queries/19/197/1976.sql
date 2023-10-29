-- see https://docs.snowflake.com/en/sql-reference/identifier-literal

create or replace database identifier('my_db');


create or replace schema identifier('my_schema');


-- case-insensitive table name specified in a string containing the fully-qualified name
create or replace table identifier('my_db.my_schema.my_table') (c1 number);


-- case-sensitive table name specified in a double-quoted string
create or replace table identifier('"my_table"') (c1 number);


show tables in schema identifier('my_schema');
