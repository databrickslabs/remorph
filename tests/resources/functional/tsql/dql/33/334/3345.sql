--Query type: DQL
SELECT Description FROM (VALUES (1, 'Aluminum and spindle'), (2, 'Steel and pedal'), (3, 'Aluminum and pedal')) AS ProductDescription(ProductDescriptionID, Description) WHERE ProductDescriptionID <> 5 AND Description LIKE '%Aluminum%spindle%
