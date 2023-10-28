DECLARE
    c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
    OPEN c1;
    ...