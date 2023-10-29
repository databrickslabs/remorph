-- see https://docs.snowflake.com/en/sql-reference/functions/boolor_agg

insert into test_boolean_agg (id, c1, c2, c3, c4) values
    (-4, false, false, false, true),
    (-3, false, true,  true,  true),
    (-2, false, false, true,  true),
    (-1, false, true,  true,  true);