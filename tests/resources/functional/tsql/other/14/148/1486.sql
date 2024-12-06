-- tsql sql:
DECLARE @CustomerCTE TABLE (CUSTKEY INT NOT NULL, PRIMARY KEY CLUSTERED (CUSTKEY), UNIQUE NONCLUSTERED (CUSTKEY), INDEX CustomNonClusteredIndex NONCLUSTERED (CUSTKEY));
WITH CustomerCTE AS (
    SELECT CUSTKEY, NATIONKEY, PHONE, ADDRESS, COMMENT
    FROM (
        VALUES (1, 1, '123-456-7890', '123 Main St', 'Comment 1'),
               (2, 2, '987-654-3210', '456 Elm St', 'Comment 2')
    ) AS CustomerTable (CUSTKEY, NATIONKEY, PHONE, ADDRESS, COMMENT)
);
SELECT * FROM CustomerCTE;
-- REMORPH CLEANUP: DROP TABLE @CustomerCTE;