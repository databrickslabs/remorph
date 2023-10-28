DECLARE
    price_to_search_for FLOAT;
    price_count INTEGER;
    c2 CURSOR FOR SELECT COUNT(*) FROM invoices WHERE price = ?;
BEGIN
    price_to_search_for := 11.11;
    OPEN c2 USING (price_to_search_for);