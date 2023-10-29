-- see https://docs.snowflake.com/en/sql-reference/functions-regexp

create table wildcards (w varchar, w2 varchar);
insert into wildcards (w, w2) values ('\\', '?');