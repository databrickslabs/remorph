--Query type: DDL
CREATE PROCEDURE dbo.InsertCustomer
    @CustomerID INTEGER,
    @Name VARCHAR(25),
    @Address VARCHAR(40),
    @NationKey INTEGER
AS
BEGIN
    SET NOCOUNT ON;

    WITH Source AS (
        SELECT @CustomerID AS CustomerID,
               @Name AS Name,
               @Address AS Address,
               @NationKey AS NationKey
    )
    MERGE INTO dbo.Customer AS tgt
    USING Source AS src
    ON tgt.CustomerID = src.CustomerID
    WHEN MATCHED THEN
        UPDATE SET Name = src.Name,
                     Address = src.Address,
                     NationKey = src.NationKey
    WHEN NOT MATCHED THEN
        INSERT (CustomerID, Name, Address, NationKey)
        VALUES (src.CustomerID, src.Name, src.Address, src.NationKey);
END