select s2, bitor_agg(k), bitor_agg(d) from bitwise_example group by s2
    order by 3;