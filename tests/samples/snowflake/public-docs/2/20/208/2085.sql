SELECT HLL(o_orderdate), HLL_ESTIMATE(HLL_IMPORT(HLL_EXPORT(HLL_ACCUMULATE(o_orderdate))))
FROM orders;

------------------+-------------------------------------------------------------------+
 HLL(O_ORDERDATE) | HLL_ESTIMATE(HLL_IMPORT(HLL_EXPORT(HLL_ACCUMULATE(O_ORDERDATE)))) |
------------------+-------------------------------------------------------------------+
 2398             | 2398                                                              |
------------------+-------------------------------------------------------------------+