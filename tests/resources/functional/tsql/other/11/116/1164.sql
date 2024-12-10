-- tsql sql:
CREATE TABLE CustomerOrder (
    geometry_col geometry,
    c_custkey INT,
    c_name VARCHAR(100),
    c_address VARCHAR(200),
    o_orderkey INT,
    o_custkey INT,
    o_totalprice DECIMAL(10, 2)
);

WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer1', 'Address1'),
               (2, 'Customer2', 'Address2'),
               (3, 'Customer3', 'Address3')
    ) AS CustomerTable (c_custkey, c_name, c_address)
),
OrderCTE AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (1, 1, 100.0),
               (2, 1, 200.0),
               (3, 2, 50.0)
    ) AS OrderTable (o_orderkey, o_custkey, o_totalprice)
)
INSERT INTO CustomerOrder (c_custkey, c_name, c_address, o_orderkey, o_custkey, o_totalprice)
SELECT C.c_custkey, C.c_name, C.c_address, O.o_orderkey, O.o_custkey, O.o_totalprice
FROM CustomerCTE C
JOIN OrderCTE O ON C.c_custkey = O.o_custkey;

UPDATE CustomerOrder
SET geometry_col = geometry::Point(100, 100, 0);

CREATE SPATIAL INDEX SIndx_CustomerOrder_geometry_col
ON CustomerOrder(geometry_col)
USING GEOMETRY_GRID
WITH (
    BOUNDING_BOX = (xmin = 0, ymin = 0, xmax = 500, ymax = 200),
    GRIDS = (LOW, LOW, MEDIUM, HIGH),
    CELLS_PER_OBJECT = 64,
    PAD_INDEX = ON
);

SELECT *
FROM CustomerOrder;
