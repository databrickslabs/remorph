-- tsql sql:
SELECT * FROM (VALUES ('regionName', 'countryName', 'cityName', 10.2, '2022-01-01', 1), ('regionName2', 'countryName2', 'cityName2', 20.2, '2022-01-02', 2)) AS sales_data(regionName, countryName, cityName, salesAmount, dateKey, productKey);
