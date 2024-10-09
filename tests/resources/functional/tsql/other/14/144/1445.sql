--Query type: DCL
DECLARE @SupplierID int = 1;
DECLARE @SupplierName varchar(200) = 'Supplier1';
DECLARE @Address varchar(max) = REPLACE(CONVERT(varchar(100), @SupplierID), '1', 'A') + @SupplierName;
DECLARE @Secret varchar(max);
WITH temp_result AS (
    SELECT @Address AS address
)
SELECT @Secret = address
FROM temp_result;
EXEC ('CREATE CREDENTIAL TPC_H_cred WITH IDENTITY = ''Supplier1'', SECRET = ''' + @Secret + ''' FOR CRYPTOGRAPHIC PROVIDER TPC_H_Prov ;');