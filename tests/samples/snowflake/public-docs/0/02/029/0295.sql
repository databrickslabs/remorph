create or replace table aggr(k int, v decimal(10,2), v2 decimal(10, 2));

insert into aggr values
    (1, 10, null),
    (2, 10, null),
    (2, 20, 22),
    (2, 25, null),
    (2, 30, 35);