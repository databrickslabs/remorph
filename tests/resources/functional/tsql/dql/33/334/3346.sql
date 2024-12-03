--Query type: DQL
SELECT Description, DiscountPct, MinQty, ISNULL(MaxQty, 0.00) AS [Max Quantity] FROM (VALUES ('Desc1', 0.1, 10, 100.00), ('Desc2', 0.2, 20, NULL)) AS SpecialOffer(Description, DiscountPct, MinQty, MaxQty);
