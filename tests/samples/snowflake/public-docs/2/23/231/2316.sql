select k, mode(v) 
    from aggr 
    group by k
    order by k;