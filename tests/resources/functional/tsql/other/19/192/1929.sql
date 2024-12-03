--Query type: DML
DECLARE supp_cursor CURSOR FOR SELECT * FROM (VALUES ('Supplier#000000001', 'Supplier#000000002')) AS Supplier(suppkey, name);
OPEN supp_cursor;
FETCH NEXT FROM supp_cursor;
-- REMORPH CLEANUP: DROP TABLE Supplier;
