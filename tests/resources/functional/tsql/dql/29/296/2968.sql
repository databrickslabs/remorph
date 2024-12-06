-- tsql sql:
SELECT r1.Name AS Region, r2.BusinessEntityID
FROM (
    VALUES (1, 'North'),
           (2, 'South'),
           (3, 'East'),
           (4, 'West')
) AS r1 (RegionID, Name)
RIGHT OUTER JOIN (
    VALUES (1, 1),
           (2, 2),
           (3, 3),
           (4, 4)
) AS r2 (RegionID, BusinessEntityID)
    ON r1.RegionID = r2.RegionID;
