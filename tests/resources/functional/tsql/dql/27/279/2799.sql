--Query type: DQL
WITH CustomerCTE AS (
    SELECT TOP 10
        c_custkey,
        c_name,
        c_address
    FROM
        customer
)
SELECT
    T2.[Order].value('.', 'nvarchar(max)') AS OrderValue
FROM
    CustomerCTE
    CROSS APPLY (
        SELECT CAST('<root><Order><OrderKey>' + CAST(o_orderkey AS VARCHAR(10)) + '</OrderKey><OrderStatus>' + o_orderstatus + '</OrderStatus></Order></root>' AS XML) AS OrderXML
    ) AS T1(Orders)
    CROSS APPLY T1.Orders.nodes('/root/Order') AS T2([Order])
