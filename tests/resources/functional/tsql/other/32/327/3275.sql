--Query type: DML
DECLARE @AvgPrice DECIMAL(8,2), @ProductCount INT;

IF (SELECT COUNT(*) FROM (VALUES ('HL Road Frame - Black, 58', 105.46), ('HL Road Frame - Red, 58', 105.46), ('HL Road Frame - Black, 62', 105.46), ('HL Road Frame - Red, 62', 105.46), ('HL Road Frame - Black, 44', 105.46), ('HL Road Frame - Red, 44', 105.46)) AS Product(Name, Price) WHERE Name LIKE 'HL Road Frame%') > 5
BEGIN
    SET @ProductCount = (SELECT COUNT(*) FROM (VALUES ('HL Road Frame - Black, 58', 105.46), ('HL Road Frame - Red, 58', 105.46), ('HL Road Frame - Black, 62', 105.46), ('HL Road Frame - Red, 62', 105.46), ('HL Road Frame - Black, 44', 105.46), ('HL Road Frame - Red, 44', 105.46)) AS Product(Name, Price) WHERE Name LIKE 'HL Road Frame%');
    SET @AvgPrice = (SELECT AVG(Price) FROM (VALUES ('HL Road Frame - Black, 58', 105.46), ('HL Road Frame - Red, 58', 105.46), ('HL Road Frame - Black, 62', 105.46), ('HL Road Frame - Red, 62', 105.46), ('HL Road Frame - Black, 44', 105.46), ('HL Road Frame - Red, 44', 105.46)) AS Product(Name, Price) WHERE Name LIKE 'HL Road Frame%');
    PRINT 'There are ' + CAST(@ProductCount AS VARCHAR(3)) + ' HL Road Frame products.';
    PRINT 'The average price of the top 5 HL Road Frame products is ' + CAST(@AvgPrice AS VARCHAR(8)) + '.';
END
ELSE
BEGIN
    SET @AvgPrice = (SELECT AVG(Price) FROM (VALUES ('HL Road Frame - Black, 58', 105.46), ('HL Road Frame - Red, 58', 105.46), ('HL Road Frame - Black, 62', 105.46), ('HL Road Frame - Red, 62', 105.46), ('HL Road Frame - Black, 44', 105.46), ('HL Road Frame - Red, 44', 105.46)) AS Product(Name, Price) WHERE Name LIKE 'HL Road Frame%');
    PRINT 'Average price of the HL Road Frame products is ' + CAST(@AvgPrice AS VARCHAR(8)) + '.';
END;

SELECT * FROM (VALUES ('HL Road Frame - Black, 58', 105.46), ('HL Road Frame - Red, 58', 105.46), ('HL Road Frame - Black, 62', 105.46), ('HL Road Frame - Red, 62', 105.46), ('HL Road Frame - Black, 44', 105.46), ('HL Road Frame - Red, 44', 105.46)) AS Product(Name, Price);
-- REMORPH CLEANUP: DROP TABLE Product;