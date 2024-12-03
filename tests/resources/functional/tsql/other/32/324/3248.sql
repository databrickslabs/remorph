--Query type: DDL
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'NewSchema')
BEGIN
    EXEC('CREATE SCHEMA NewSchema');
END

-- Create the Address table in the NewSchema if it does not exist
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Address' AND schema_id = SCHEMA_ID('NewSchema'))
BEGIN
    CREATE TABLE NewSchema.Address
    (
        AddressID INT,
        AddressLine1 VARCHAR(120),
        City VARCHAR(60),
        StateProvinceID INT,
        PostalCode VARCHAR(30)
    );
END

-- Create the Person.Address table if it does not exist (assuming it's in the dbo schema for simplicity)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Address' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.Address
    (
        AddressID INT,
        AddressLine1 VARCHAR(120),
        City VARCHAR(60),
        StateProvinceID INT,
        PostalCode VARCHAR(30)
    );
END

-- Transfer the table to the new schema
ALTER SCHEMA NewSchema TRANSFER dbo.Address;

-- Display a message using a Table Value Constructor
SELECT 'Transferred Successfully' AS Message;

-- Display the data from the transferred table
SELECT * FROM NewSchema.Address;

-- REMORPH CLEANUP: DROP TABLE NewSchema.Address;
-- REMORPH CLEANUP: DROP TABLE dbo.Address;
-- REMORPH CLEANUP: DROP SCHEMA NewSchema;
