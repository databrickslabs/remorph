--Query type: DML
DECLARE @var1 VARCHAR(30);
SELECT @var1 = 'Generic Name';
SELECT @var1 = Name
FROM (
    VALUES ('Road-150 Red, 48')
) AS ProductCTE(Name)
WHERE Name = 'Road-150 Red, 48';
SELECT @var1 AS 'ProductName';
