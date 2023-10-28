select k, v, mode(v) over (partition by k) 
    from aggr 
    order by k, v;