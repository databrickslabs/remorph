--Query type: DCL
WITH all_columns_cte AS (
    SELECT column_name
    FROM (
        VALUES ('column1'),
               ('column2'),
               ('column3')
    ) AS all_columns (column_name)
)
SELECT *
FROM all_columns_cte;

SELECT *
FROM (
    VALUES ('column1'),
           ('column2'),
           ('column3')
) AS all_columns (column_name);

CREATE TABLE #demo_table (
    column_name sysname
);

INSERT INTO #demo_table (
    column_name
)
VALUES ('column1'),
       ('column2'),
       ('column3');

SELECT *
FROM #demo_table;

-- REMORPH CLEANUP: DROP TABLE #demo_table;
