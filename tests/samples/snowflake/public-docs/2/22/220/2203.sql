select s2, bitxor_agg(k), bitxor_agg(d) from bitwise_example group by s2
    order by 3;