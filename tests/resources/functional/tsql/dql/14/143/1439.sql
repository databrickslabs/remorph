--Query type: DQL
DECLARE @ORDER_STATUS VARCHAR(3) = 'OFF';
IF ( (1024 & @@OPTIONS) = 1024 )
    SET @ORDER_STATUS = 'ON';
SELECT o_orderstatus, @ORDER_STATUS AS ORDER_STATUS
FROM (
    VALUES ('O', 1), ('F', 2)
) AS o (o_orderstatus, o_orderkey);
