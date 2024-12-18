-- tsql sql:
CREATE TABLE #data_retention_table
(
    dbdatetime2 datetime2(7),
    product_code int,
    value char(10)
);

INSERT INTO #data_retention_table
VALUES
    (
        CAST('2022-01-01 00:00:00.0000000' AS datetime2(7)),
        1,
        'value1'
    ),
    (
        CAST('2022-01-08 00:00:00.0000000' AS datetime2(7)),
        2,
        'value2'
    ),
    (
        CAST('2022-01-15 00:00:00.0000000' AS datetime2(7)),
        3,
        'value3'
    ),
    (
        CAST('2022-01-22 00:00:00.0000000' AS datetime2(7)),
        4,
        'value4'
    );

SELECT *
FROM #data_retention_table;

-- REMORPH CLEANUP: DROP TABLE #data_retention_table;
