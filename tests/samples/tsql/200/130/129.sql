SELECT st.Name AS Territory,
    sp.BusinessEntityID
FROM Sales.SalesTerritory AS st
RIGHT OUTER JOIN Sales.SalesPerson AS sp
    ON st.TerritoryID = sp.TerritoryID;