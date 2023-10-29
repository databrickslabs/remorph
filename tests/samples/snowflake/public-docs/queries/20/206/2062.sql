-- see https://docs.snowflake.com/en/sql-reference/functions/booland_agg

select 
      id,
      booland_agg(c1) OVER (PARTITION BY (id > 0)),
      booland_agg(c2) OVER (PARTITION BY (id > 0)),
      booland_agg(c3) OVER (PARTITION BY (id > 0)),
      booland_agg(c4) OVER (PARTITION BY (id > 0))
    from test_boolean_agg
    order by id;