-- see https://docs.snowflake.com/en/sql-reference/functions/boolor_agg

select boolor_agg(c1), boolor_agg(c2), boolor_agg(c3), boolor_agg(c4)
    from test_boolean_agg;