DECLARE @bulk_cmd VARCHAR(1000);
SET @bulk_cmd = 'BULK INSERT AdventureWorks2022.Sales.SalesOrderDetail
FROM ''<drive>:\<path>\<filename>''
WITH (ROWTERMINATOR = '''+CHAR(10)+''')';
EXEC(@bulk_cmd);

BULK INSERT MyTable
FROM 'D:\data.csv'
WITH
( CODEPAGE = '65001'
   , DATAFILETYPE = 'char'
   , FIELDTERMINATOR = ','
);