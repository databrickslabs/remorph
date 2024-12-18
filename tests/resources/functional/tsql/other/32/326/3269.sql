-- tsql sql:
SELECT *
INTO t2
FROM (
    VALUES (
        1,
        '2022-01-01'
    )
) AS t (c3, c4);

SELECT *
FROM t2;
-- REMORPH CLEANUP: DROP TABLE t2;
