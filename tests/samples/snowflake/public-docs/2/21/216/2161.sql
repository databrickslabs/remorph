select 
      id,
      boolor_agg(c1) OVER (PARTITION BY (id > 0)),
      boolor_agg(c2) OVER (PARTITION BY (id > 0)),
      boolor_agg(c3) OVER (PARTITION BY (id > 0)),
      boolor_agg(c4) OVER (PARTITION BY (id > 0))
    from test_boolean_agg
    order by id;