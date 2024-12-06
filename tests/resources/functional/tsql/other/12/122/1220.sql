-- tsql sql:
CREATE TABLE Sales
(
    Country VARCHAR(50),
    Region VARCHAR(50),
    Sales INT
);

INSERT INTO Sales
VALUES
    (N'Canada', N'Alberta', 100),
    (N'Canada', N'British Columbia', 200),
    (N'Canada', N'British Columbia', 300),
    (N'United States', N'Montana', 100);

WITH Countries AS
(
    SELECT CountryName, RegionName
    FROM (
        VALUES
            (N'Canada', N'Alberta'),
            (N'Canada', N'British Columbia'),
            (N'United States', N'Montana')
    ) C (CountryName, RegionName)
),
SalesData AS
(
    SELECT Country, Region, Sales
    FROM (
        VALUES
            (N'Canada', N'Alberta', 100),
            (N'Canada', N'British Columbia', 200),
            (N'Canada', N'British Columbia', 300),
            (N'United States', N'Montana', 100)
    ) S (Country, Region, Sales)
)
SELECT C.CountryName, C.RegionName, SUM(SD.Sales) AS TotalSales
FROM Countries C
JOIN SalesData SD ON C.CountryName = SD.Country AND C.RegionName = SD.Region
GROUP BY C.CountryName, C.RegionName;
