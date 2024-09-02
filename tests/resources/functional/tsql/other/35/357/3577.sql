--Query type: DCL
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'MySchema')
BEGIN
    EXEC('CREATE SCHEMA MySchema');
END

IF EXISTS (SELECT * FROM sys.database_principals WHERE name = 'ZJohnDoe')
BEGIN
    REVOKE CONTROL ON SCHEMA::MySchema TO ZJohnDoe;
END

SELECT * FROM sys.schemas WHERE name = 'MySchema';

CREATE TABLE MySchema.MyTable (
    ID INT,
    Name VARCHAR(100)
);
INSERT INTO MySchema.MyTable (ID, Name) VALUES (1, 'John Doe');
SELECT * FROM MySchema.MyTable;
-- REMORPH CLEANUP: DROP TABLE MySchema.MyTable;
-- REMORPH CLEANUP: DROP SCHEMA MySchema;