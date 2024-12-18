-- tsql sql:
WITH customer_hierarchy AS ( SELECT CONVERT(VARCHAR(10), c_custkey) + '.' + CONVERT(VARCHAR(10), c_nationkey) AS hierarchy, c_custkey, c_nationkey FROM customer ) SELECT hierarchy.ToString() AS Text_Hierarchy, hierarchy.GetLevel() AS CustLevel, * FROM customer_hierarchy;
