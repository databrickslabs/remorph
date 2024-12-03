--Query type: DML
DECLARE @Orders TABLE (orderKey INT, totalprice INT, orderstatus CHAR(1));
INSERT INTO @Orders (orderKey, totalprice, orderstatus)
VALUES (1, 500, 'O'), (2, 200, 'C'), (3, 300, 'O');
DECLARE @t TABLE (orderKey INT);
UPDATE @Orders
SET totalprice = 1000
OUTPUT inserted.orderKey INTO @t (orderKey)
WHERE orderKey = 1 AND orderstatus = 'O';
IF (SELECT COUNT(*) FROM @t) = 0
BEGIN
    RAISERROR ('error changing row with orderKey = %d', 16, 1, 1);
END;
SELECT * FROM @t;
SELECT * FROM @Orders;
