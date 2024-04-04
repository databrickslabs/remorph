
-- snowflake sql:
SELECT A.COL1, A.COL2, B.COL3, B.COL4 FROM 
                            (SELECT COL1, COL2 FROM TABLE1) A, 
                            (SELECT VALUE:PRICE::FLOAT AS COL3, COL4 FROM 
                            (SELECT * FROM TABLE2 ) AS K
                            ) B 
                            WHERE A.COL1 = B.COL4;

-- databricks sql:
SELECT a.col1, a.col2, b.col3, b.col4 FROM (SELECT col1, col2 FROM table1) AS a, 
        (SELECT CAST(value.price AS DOUBLE) AS col3, col4 
        FROM (SELECT * FROM table2) AS k) AS b WHERE a.col1 = b.col4;
