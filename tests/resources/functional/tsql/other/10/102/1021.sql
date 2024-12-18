-- tsql sql:
CREATE TABLE Supplier (NationKey INT, Name VARCHAR(50));
INSERT INTO Supplier (NationKey, Name)
SELECT NationKey, Name
FROM (VALUES (1, 'USA'), (2, 'Canada')) AS Supplier (NationKey, Name);
CREATE INDEX IX_Supplier_NationKey ON Supplier (NationKey);
SELECT * FROM Supplier;
-- REMORPH CLEANUP: DROP INDEX IX_Supplier_NationKey ON Supplier;
-- REMORPH CLEANUP: DROP TABLE Supplier;
