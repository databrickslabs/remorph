--Query type: DML
WITH src AS (
    SELECT L_ORDERKEY, SUM(CONVERT(int, L_QUANTITY)) AS Quantity
    FROM (
        SELECT L_ORDERKEY, L_QUANTITY
        FROM (
            VALUES ('1', '10'),
                   ('2', '20'),
                   ('3', '30')
        ) AS Lineitem (L_ORDERKEY, L_QUANTITY)
        INNER JOIN (
            VALUES ('1', '1996-03-01'),
                   ('2', '1996-03-15'),
                   ('3', '1996-03-31')
        ) AS Orders (O_ORDERKEY, O_ORDERDATE)
            ON Lineitem.L_ORDERKEY = Orders.O_ORDERKEY
        WHERE Orders.O_ORDERDATE BETWEEN '1996-03-01' AND '1996-03-31'
    ) AS subquery
    GROUP BY L_ORDERKEY
)
MERGE #UpdatedLineitem AS target
USING src AS source
    ON target.L_ORDERKEY = source.L_ORDERKEY
WHEN MATCHED AND target.L_QUANTITY - source.Quantity >= 0
    THEN UPDATE SET target.L_QUANTITY = target.L_QUANTITY - source.Quantity
WHEN MATCHED AND target.L_QUANTITY - source.Quantity <= 0
    THEN DELETE
OUTPUT $action, Inserted.L_ORDERKEY, Inserted.L_PARTKEY, Inserted.L_SUPPKEY, Inserted.L_LINENUMBER, Inserted.L_QUANTITY AS NewQuantity, Deleted.L_QUANTITY AS PreviousQuantity
INTO #Changes;
INSERT INTO #UpdatedLineitem (L_ORDERKEY, L_PARTKEY, L_SUPPKEY, L_LINENUMBER, L_QUANTITY)
SELECT L_ORDERKEY, L_PARTKEY, L_SUPPKEY, L_LINENUMBER, NewQuantity
FROM #Changes
WHERE Action = 'UPDATE';
SELECT * FROM #UpdatedLineitem;
