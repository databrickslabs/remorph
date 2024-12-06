-- tsql sql:
SELECT o_orderkey, o_orderdate, CAST(o_orderdate AS datetime) AT TIME ZONE 'Pacific Standard Time' AS o_orderdate_TimeZonePST, CAST(o_orderdate AS datetime) AT TIME ZONE 'Pacific Standard Time' AT TIME ZONE 'Central European Standard Time' AS o_orderdate_TimeZoneCET FROM (VALUES (1, '2022-01-01'), (2, '2022-01-02')) AS orders (o_orderkey, o_orderdate);
