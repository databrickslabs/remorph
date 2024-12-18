-- tsql sql:
WITH SalesCTE AS (
    SELECT
        o_orderkey,
        o_custkey,
        o_orderstatus,
        o_totalprice,
        o_orderdate,
        o_orderpriority,
        o_clerk,
        o_shippriority,
        o_comment,
        ROW_NUMBER() OVER (
            PARTITION BY o_orderkey
            ORDER BY o_orderdate
        ) AS RowNum
    FROM
    (
        VALUES
        (
            1,
            1,
            'O',
            100.00,
            '2022-01-01',
            '1-URGENT',
            'Clerk1',
            1,
            'Comment1'
        ),
        (
            2,
            2,
            'O',
            200.00,
            '2022-01-02',
            '2-HIGH',
            'Clerk2',
            2,
            'Comment2'
        ),
        (
            3,
            3,
            'O',
            300.00,
            '2022-01-03',
            '3-MEDIUM',
            'Clerk3',
            3,
            'Comment3'
        )
    ) AS SalesData(
        o_orderkey,
        o_custkey,
        o_orderstatus,
        o_totalprice,
        o_orderdate,
        o_orderpriority,
        o_clerk,
        o_shippriority,
        o_comment
    )
)
SELECT * FROM SalesCTE;
