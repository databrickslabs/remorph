--Query type: DDL
CREATE TABLE #SupplierTable
(
    geography_col1 geography,
    supplier_name nvarchar(50)
);

INSERT INTO #SupplierTable (geography_col1, supplier_name)
SELECT geography::Point(
        CAST(PARSENAME(REPLACE(supplier_address, ' ', '.'), 2) AS float),
        CAST(PARSENAME(REPLACE(supplier_address, ' ', '.'), 1) AS float),
        4326
    ),
    supplier_name
FROM (
    VALUES
        ('37.7749 -122.4194', 'Anytown', 'USA', 'North America', 'Supplier1'),
        ('45.5236 -122.6750', 'Othertown', 'Canada', 'North America', 'Supplier2')
) AS Supplier(
    supplier_address,
    supplier_city,
    supplier_nation,
    supplier_region,
    supplier_name
);

CREATE SPATIAL INDEX SIndx_Supplier_geography_col1
ON #SupplierTable (geography_col1)
USING GEOGRAPHY_GRID
WITH (
    GRIDS = (HIGH, MEDIUM, LOW, MEDIUM),
    CELLS_PER_OBJECT = 128,
    PAD_INDEX = OFF
);

SELECT *
FROM #SupplierTable;
-- REMORPH CLEANUP: DROP TABLE #SupplierTable;
