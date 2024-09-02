--Query type: DQL
DECLARE @AR_ORDERSTATUS VARCHAR(3) = 'OFF';
IF ( (16 & @@OPTIONS) = 16 )
    SET @AR_ORDERSTATUS = 'ON';

SELECT
    CASE
        WHEN (16 & @@OPTIONS) = 16 THEN 'ON'
        ELSE 'OFF'
    END AS AR_ORDERSTATUS,
    o_orderstatus,
    o_totalprice
FROM
    (
        VALUES
            (1, 'O', 100.00),
            (2, 'O', 200.00),
            (3, 'O', 300.00)
    ) AS orders (o_orderkey, o_orderstatus, o_totalprice)
WHERE
    o_orderstatus = 'O'
    AND o_totalprice > 150.00;