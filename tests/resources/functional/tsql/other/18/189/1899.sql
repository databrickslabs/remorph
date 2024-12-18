-- tsql sql:
DECLARE @v2 INT;

WITH Test2 AS (
  SELECT BusinessEntityID
  FROM (
    VALUES (1), (2), (3)
  ) AS Employee2(BusinessEntityID)
  UNION ALL
  SELECT BusinessEntityID
  FROM (
    VALUES (4), (5), (6)
  ) AS EmployeeAddress2(BusinessEntityID)
)

SELECT @v2 = BusinessEntityID
FROM Test2;

SELECT @v2;

-- REMORPH CLEANUP: DROP TABLE Employee2;
-- REMORPH CLEANUP: DROP TABLE EmployeeAddress2;
