--Query type: DML
CREATE TABLE #CitiesTemp (Name nvarchar(50), Location geography);
INSERT INTO #CitiesTemp (Name, Location)
SELECT Name, Location
FROM (VALUES ('New York', GEOGRAPHY::Point(40.7128, 74.0060, 4326))) AS subquery(Name, Location);
UPDATE #CitiesTemp
SET Location = Location.SetXY(23.5, 23.5)
WHERE Name = 'New York';
SELECT * FROM #CitiesTemp;
-- REMORPH CLEANUP: DROP TABLE #CitiesTemp;
