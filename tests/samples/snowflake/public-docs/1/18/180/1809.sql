create table MYTABLE1 (id int);

create table MYTABLE2(id int);

create stream MYSTREAM on table MYTABLE1;

insert into MYTABLE1 values (1);

-- returns true because the stream contains change tracking information
select system$stream_has_data('MYSTREAM');


 -- consume the stream
begin;
insert into MYTABLE2 select id from MYSTREAM;
commit;

-- returns false because the stream was consumed
select system$stream_has_data('MYSTREAM');
