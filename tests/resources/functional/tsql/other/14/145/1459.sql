--Query type: DML
DECLARE @CustomerID AS NVARCHAR(256);
DECLARE @CompanyName AS NVARCHAR(50);

DECLARE Customer_Cursor CURSOR FOR
SELECT c_customer_id, c_name
FROM (
  VALUES ('Customer#000000001', 'Customer#000000001')
) AS CustomerCTE (c_customer_id, c_name)
WHERE c_name = 'Customer#000000001';

OPEN Customer_Cursor;
FETCH NEXT FROM Customer_Cursor INTO @CustomerID, @CompanyName;

WHILE @@FETCH_STATUS = 0
BEGIN
    PRINT '   ' + @CustomerID + '      ' + @CompanyName;
    FETCH NEXT FROM Customer_Cursor INTO @CustomerID, @CompanyName;
END;

CLOSE Customer_Cursor;
DEALLOCATE Customer_Cursor;