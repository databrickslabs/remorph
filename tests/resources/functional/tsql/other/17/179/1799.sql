--Query type: DML
WITH hidCTE AS (SELECT HIERARCHYID::GetRoot() AS hid)
SELECT hid.ToString() AS hid_string
FROM hidCTE
OPTION (MAXRECURSION 0);
