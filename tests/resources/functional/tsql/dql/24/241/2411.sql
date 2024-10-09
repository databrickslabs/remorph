--Query type: DQL
SELECT APPROX_COUNT_DISTINCT(L_OrderKey) AS Approx_Distinct_LineItemOrderKey FROM (VALUES (1, 10), (2, 20), (3, 30), (4, 40), (5, 50)) AS LineItem(L_OrderKey, L_Quantity);