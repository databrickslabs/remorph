-- tsql sql:
DECLARE @Grouping nvarchar(50);
SET @Grouping = N'CountryRegionCode Total';

WITH SalesData AS (
    SELECT
        T.[Group],
        T.CountryRegionCode,
        S.Name AS N'Store',
        (
            SELECT P.FirstName + ' ' + P.LastName
            FROM (
                VALUES ('John', 'Doe', 1),
                       ('Jane', 'Doe', 2),
                       ('Bob', 'Smith', 3)
            ) AS P (FirstName, LastName, BusinessEntityID)
            WHERE P.BusinessEntityID = H.SalesPersonID
        ) AS N'Sales Person',
        SUM(TotalDue) AS N'TotalSold'
    FROM (
        VALUES ('North America', 'USA', 'New York'),
               ('North America', 'Canada', 'Toronto'),
               ('South America', 'Brazil', 'Rio de Janeiro')
    ) AS T ([Group], CountryRegionCode, Name)
    INNER JOIN (
        VALUES ('New York', 1),
               ('Toronto', 2),
               ('Rio de Janeiro', 3)
    ) AS S (Name, BusinessEntityID) ON T.Name = S.Name
    INNER JOIN (
        VALUES (1, 1, 100.0),
               (2, 2, 200.0),
               (3, 3, 300.0)
    ) AS H (SalesPersonID, CustomerID, TotalDue) ON S.BusinessEntityID = H.CustomerID
    GROUP BY
        T.[Group],
        T.CountryRegionCode,
        S.Name,
        H.SalesPersonID
)

SELECT
    MAX(T.[Group]) AS [Group],
    MAX(T.CountryRegionCode) AS CountryRegionCode,
    MAX(T.Store) AS Store,
    MAX(T.[Sales Person]) AS [Sales Person],
    MAX(T.TotalSold) AS TotalSold,
    CAST(GROUPING(T.[Group]) AS char(1)) + CAST(GROUPING(T.CountryRegionCode) AS char(1)) + CAST(GROUPING(T.Store) AS char(1)) + CAST(GROUPING(T.[Sales Person]) AS char(1)) AS N'GROUPING base-2',
    GROUPING_ID((T.[Group]), (T.CountryRegionCode), (T.Store), (T.[Sales Person])) AS N'GROUPING_ID',
    CASE
        WHEN GROUPING_ID((T.[Group]), (T.CountryRegionCode), (T.Store), (T.[Sales Person])) = 15 THEN N'Grand Total'
        WHEN GROUPING_ID((T.[Group]), (T.CountryRegionCode), (T.Store), (T.[Sales Person])) = 14 THEN N'SalesPerson Total'
        WHEN GROUPING_ID((T.[Group]), (T.CountryRegionCode), (T.Store), (T.[Sales Person])) = 13 THEN N'Store Total'
        WHEN GROUPING_ID((T.[Group]), (T.CountryRegionCode), (T.Store), (T.[Sales Person])) = 12 THEN N'Store SalesPerson Total'
        WHEN GROUPING_ID((T.[Group]), (T.CountryRegionCode), (T.Store), (T.[Sales Person])) = 11 THEN N'CountryRegionCode Total'
        WHEN GROUPING_ID((T.[Group]), (T.CountryRegionCode), (T.Store), (T.[Sales Person])) = 7 THEN N'Group Total'
        ELSE N'Error'
    END AS N'Level'
FROM SalesData AS T
GROUP BY
    GROUPING SETS ((T.Store, T.[Sales Person]), (T.[Sales Person]), (T.Store), (T.[Group]), (T.CountryRegionCode), ())
HAVING
    GROUPING_ID((T.[Group]), (T.CountryRegionCode), (T.Store), (T.[Sales Person])) = (
        CASE @Grouping
            WHEN N'Grand Total' THEN 15
            WHEN N'SalesPerson Total' THEN 14
            WHEN N'Store Total' THEN 13
            WHEN N'Store SalesPerson Total' THEN 12
            WHEN N'CountryRegionCode Total' THEN 11
            WHEN N'Group Total' THEN 7
            ELSE 0
        END
    )
ORDER BY
    GROUPING_ID(T.Store, T.[Sales Person]),
    GROUPING_ID((T.[Group]), (T.CountryRegionCode), (T.Store), (T.[Sales Person])) ASC;
