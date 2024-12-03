--Query type: DQL
WITH RegionCTE AS (SELECT RegionID, RegionName FROM dbo.GetRegions())
SELECT r.RegionID, r.RegionName, r.MgrID, e.EmpID, e.EmpLastName, e.EmpSalary
FROM RegionCTE r
OUTER APPLY dbo.GetReports(r.MgrID) e;
