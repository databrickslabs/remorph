select count(distinct o_orderdate) from orders;

-----------------------------+
 COUNT(DISTINCT O_ORDERDATE) |
-----------------------------+
 2406                        |
-----------------------------+

select count(o_orderdate)
from (select o_orderdate, hash_agg(distinct o_custkey)
      from orders
      where o_orderstatus <> 'F'
      group by 1
      intersect
      select o_orderdate, hash_agg(distinct o_custkey)
      from orders
      where o_orderstatus <> 'P'
      group by 1);

--------------------+
 COUNT(O_ORDERDATE) |
--------------------+
 1143               |
--------------------+