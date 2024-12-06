-- tsql sql:
CREATE TABLE t1 (
    charcol CHAR(16) NULL,
    varcharcol VARCHAR(16) NULL,
    varbinarycol VARBINARY(8)
);

INSERT INTO t1 (
    charcol,
    varcharcol,
    varbinarycol
)
SELECT
    CAST('Hello' AS CHAR(16)) AS charcol,
    CAST('World' AS VARCHAR(16)) AS varcharcol,
    CAST(0x12345678 AS VARBINARY(8)) AS varbinarycol
FROM (
    VALUES (
        1
    )
) AS temp_result (id);
