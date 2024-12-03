--Query type: DML
CREATE TABLE #CityData (Name VARCHAR(255), Location VARCHAR(255));
INSERT INTO #CityData (Name, Location) VALUES ('Anchorage', '12.3:46.2'), ('New York', '20.2:50.2'), ('Los Angeles', '30.3:60.3');
UPDATE #CityData SET Location = CONVERT(VARCHAR(255), CONVERT(Point, Location)) WHERE Name = 'Anchorage';
SELECT * FROM #CityData;
-- REMORPH CLEANUP: DROP TABLE #CityData;
