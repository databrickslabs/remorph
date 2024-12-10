-- tsql sql:
WITH OrdersCTE AS (
    SELECT
        o_orderdate,
        o_orderkey,
        YEAR(o_orderdate) AS [Year],
        MONTH(o_orderdate) AS [Month]
    FROM
    (
        VALUES
            ('1992-01-01', 1),
            ('1992-02-01', 2),
            ('1992-03-01', 3)
    ) AS o (o_orderdate, o_orderkey)
    WHERE
        o_orderdate < '1993-12-31'
)
SELECT * FROM OrdersCTE;
