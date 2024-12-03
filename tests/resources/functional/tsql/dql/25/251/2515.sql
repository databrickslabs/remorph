--Query type: DQL
WITH CustomerCTE AS (SELECT 'Customer1' AS Name, 'Sales' AS JobTitle),
			OrderCTE AS (SELECT 'Order1' AS OrderName, 'Customer1' AS CustomerName),
			LineitemCTE AS (SELECT 'Lineitem1' AS LineitemName, 'Order1' AS OrderName)
SELECT
			C.Name,
			O.OrderName,
			GROUPING_ID(C.Name, O.OrderName) AS [Grouping Level],
			COUNT(L.LineitemName) AS [Order Count]
FROM
			CustomerCTE AS C
			INNER JOIN OrderCTE AS O ON C.Name = O.CustomerName
			INNER JOIN LineitemCTE AS L ON O.OrderName = L.OrderName
WHERE
			L.LineitemName IS NOT NULL
			AND C.Name IN ('Customer1', 'Customer2')
GROUP BY
			ROLLUP(C.Name, O.OrderName)
