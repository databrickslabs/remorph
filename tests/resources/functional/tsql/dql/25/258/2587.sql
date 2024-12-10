-- tsql sql:
WITH RegionCTE AS (
    SELECT RegionID, RegionName
    FROM (
        VALUES (1, 'North'),
               (2, 'South')
    ) AS Region(RegionID, RegionName)
)
SELECT r.RegionID, r.RegionName, e.EmpID, e.EmpLastName, e.EmpSalary
FROM RegionCTE r
CROSS APPLY dbo.GetRegionEmployees(r.RegionID) e
