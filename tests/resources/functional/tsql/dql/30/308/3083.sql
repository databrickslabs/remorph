--Query type: DQL
SELECT ProductKey, ProductName, ProductSubcategoryKey, ProductCategoryKey FROM (VALUES (1, 'Product A', 1, 1), (2, 'Product B', 2, 1), (3, 'Product C', 3, 2)) AS ProductDim(ProductKey, ProductName, ProductSubcategoryKey, ProductCategoryKey);
