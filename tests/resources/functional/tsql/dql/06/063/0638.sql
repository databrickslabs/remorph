-- tsql sql:
DECLARE customer_cursor CURSOR FOR SELECT c_custkey FROM (VALUES (1),(2),(3)) AS customers(c_custkey);
DECLARE @customer_key INT;
OPEN customer_cursor;
FETCH NEXT FROM customer_cursor INTO @customer_key;
