-- see https://docs.snowflake.com/en/sql-reference/functions/boolxor_agg

select boolxor_agg(c1), boolxor_agg(c2), boolxor_agg(c3), boolxor_agg(c4)
    from test_boolean_agg;