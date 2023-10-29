-- see https://docs.snowflake.com/en/sql-reference/functions/percentile_cont

create or replace table aggr(k int, v decimal(10,2));
insert into aggr (k, v) values
    (0,  0),
    (0, 10),
    (0, 20),
    (0, 30),
    (0, 40),
    (1, 10),
    (1, 20),
    (2, 10),
    (2, 20),
    (2, 25),
    (2, 30),
    (3, 60),
    (4, NULL);