-- see https://docs.snowflake.com/en/sql-reference/functions/percentile_disc

select k, percentile_disc(0.25) within group (order by v) 
  from aggr 
  group by k
  order by k;