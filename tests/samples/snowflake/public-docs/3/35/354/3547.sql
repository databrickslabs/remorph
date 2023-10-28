use schema identifier(?);

create or replace table identifier(?) (c1 number);

insert into identifier(?) values (?), (?), (?);

select t2.c1 from identifier(?) as t1, identifier(?) as t2 where t1.c1 = t2.c1 and t1.c1 > (?);

drop table identifier(?);