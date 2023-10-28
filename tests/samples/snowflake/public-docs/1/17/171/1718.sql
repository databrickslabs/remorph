-- Prepare example
create or replace table overlap (id number, a string);

insert into overlap values (1,',abc,def,ghi,jkl,');
insert into overlap values (2,',abc,,def,,ghi,,jkl,');

select * from overlap;

select id, regexp_substr(a,'[[:punct:]][[:alnum:]]+[[:punct:]]', 1, 2) as result from overlap;
