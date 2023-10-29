-- see https://docs.snowflake.com/en/sql-reference/functions/boolor_agg

create or replace table test_boolean_agg(
    id integer,
    c1 boolean, 
    c2 boolean,
    c3 boolean,
    c4 boolean
    );

insert into test_boolean_agg (id, c1, c2, c3, c4) values 
    (1, true, true,  true,  false),
    (2, true, false, false, false),
    (3, true, true,  false, false),
    (4, true, false, false, false);