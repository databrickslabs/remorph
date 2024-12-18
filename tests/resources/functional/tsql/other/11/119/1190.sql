-- tsql sql:
CREATE TABLE Orders_PDW
WITH (DISTRIBUTION = REPLICATE)
AS
SELECT o_orderkey, o_custkey, o_orderstatus
FROM (
VALUES (1, 1, 'O'),
(2, 2, 'O'),
(3, 3, 'O')
) AS Orders(o_orderkey, o_custkey, o_orderstatus);
-- REMORPH CLEANUP: DROP TABLE Orders_PDW;
