--Query type: DML
CREATE TABLE #RegionTemp
(
    CountryRegionName nvarchar(50),
    RegionCode nvarchar(10)
);

INSERT INTO #RegionTemp (CountryRegionName, RegionCode)
SELECT 'United States of America', 'USA'
UNION ALL
SELECT 'Canada', 'CAN';

UPDATE #RegionTemp
SET CountryRegionName = 'United States'
WHERE RegionCode = 'USA';

SELECT *
FROM #RegionTemp;

-- REMORPH CLEANUP: DROP TABLE #RegionTemp;