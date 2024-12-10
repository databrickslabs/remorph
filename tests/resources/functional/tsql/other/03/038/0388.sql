-- tsql sql:
CREATE TABLE dbo.Supplier
(
    Name VARCHAR(50),
    Address VARCHAR(100)
);

INSERT INTO dbo.Supplier (Name, Address)
VALUES
    ('Supplier1', 'Address1'),
    ('Supplier2', 'Address2');

SELECT *
FROM dbo.Supplier;

-- REMORPH CLEANUP: DROP TABLE dbo.Supplier;
