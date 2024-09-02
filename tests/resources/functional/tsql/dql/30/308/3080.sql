--Query type: DQL
DECLARE @SupplierTimeZone sysname = 'Eastern Standard Time';

WITH SupplierOrders AS (
  SELECT SupplierID, CAST(OrderDate AS datetime) AS OrderDate
  FROM (
    VALUES (
      (1, '2022-01-01 12:00:00'),
      (2, '2022-01-02 13:00:00'),
      (3, '2022-01-03 14:00:00')
    )
  ) AS SupplierOrders (SupplierID, OrderDate)
)

SELECT
  SupplierID,
  OrderDate,
  OrderDate AT TIME ZONE 'Pacific Standard Time' AS OrderDate_TimeZonePST,
  OrderDate AT TIME ZONE 'Pacific Standard Time' AT TIME ZONE 'Eastern Standard Time' AS OrderDate_TimeZoneSupplier
FROM SupplierOrders;