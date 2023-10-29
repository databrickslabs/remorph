-- see https://docs.snowflake.com/en/sql-reference/functions/booland_agg

select booland_agg(c1), booland_agg(c2), booland_agg(c3), booland_agg(c4)
    from test_boolean_agg;