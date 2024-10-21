--Query type: DML
DECLARE @E TABLE (EmployeeKey INT, BaseRate DECIMAL(10, 2));
INSERT INTO @E (EmployeeKey, BaseRate)
VALUES
    (1, 100.00),
    (2, 200.00),
    (3, 300.00);
UPDATE @E
SET BaseRate = BaseRate * 2;
SELECT *
FROM @E;
-- REMORPH CLEANUP: DROP TABLE @E;