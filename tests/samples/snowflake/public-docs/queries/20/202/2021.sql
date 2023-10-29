-- see https://docs.snowflake.com/en/sql-reference/functions/system_stream_get_table_timestamp

create table MYTABLE1 (id int);

create table MYTABLE2(id int);

create or replace stream MYSTREAM on table MYTABLE1;

insert into MYTABLE1 values (1);

-- consume the stream
begin;
insert into MYTABLE2 select id from MYSTREAM;
commit;

-- return the current offset for the stream
select system$stream_get_table_timestamp('MYSTREAM');