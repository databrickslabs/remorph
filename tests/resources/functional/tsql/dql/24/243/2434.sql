-- tsql sql:
WITH CustomerCTE AS ( SELECT c_custkey, c_nationkey FROM (VALUES (1, 1), (2, 2), (3, 3)) AS Customer(c_custkey, c_nationkey)) SELECT c_custkey, c_nationkey FROM CustomerCTE ORDER BY CASE c_nationkey WHEN 1 THEN c_custkey END DESC, CASE WHEN c_nationkey = 2 THEN c_custkey END