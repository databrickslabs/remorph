-- tsql sql:
CREATE FUNCTION get_total_revenue()
RETURNS decimal(10, 2)
AS
BEGIN
    RETURN (
        SELECT SUM(l_extendedprice * l_discount)
        FROM (
            VALUES (1, 10.0, 0.1),
                   (2, 20.0, 0.2)
        ) AS lineitem(l_orderkey, l_extendedprice, l_discount)
    );
END;
