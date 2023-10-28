select k, percentile_cont(0.25) within group (order by v) 
  from aggr 
  group by k
  order by k;