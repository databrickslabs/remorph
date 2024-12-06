-- tsql sql:
DECLARE @index_exists BIT;

WITH temp_object_id AS (
    SELECT OBJECT_ID(N'dbo.Supplier') AS object_id
)

SELECT @index_exists = CASE
    WHEN EXISTS (
        SELECT name
        FROM (
            VALUES ('FISupplierWithNationID')
        ) AS temp_index (name)
        INNER JOIN temp_object_id ON 1 = 1
        WHERE name = N'FISupplierWithNationID'
    ) THEN 1
    ELSE 0
END;

IF @index_exists = 1
    DROP INDEX FISupplierWithNationID ON dbo.Supplier;

CREATE TABLE dbo.Supplier (
    SupplierID INT,
    Name VARCHAR(50)
);
