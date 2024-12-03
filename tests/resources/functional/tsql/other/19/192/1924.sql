--Query type: DML
DECLARE Supplier_Cursor CURSOR FOR
SELECT s_name, s_address
FROM (
    VALUES ('Supplier#000000001', '1313 13th St.'),
    ('Supplier#000000002', '123 Main St.')
) AS Suppliers(s_name, s_address)
WHERE s_name LIKE 'Supplier#000000001%';

OPEN Supplier_Cursor;

FETCH NEXT FROM Supplier_Cursor;

WHILE @@FETCH_STATUS = 0
BEGIN
    FETCH NEXT FROM Supplier_Cursor;
END;

CLOSE Supplier_Cursor;

DEALLOCATE Supplier_Cursor;

-- REMORPH CLEANUP: DROP TABLE Suppliers;
