-- tsql sql:
CREATE TABLE #temp_result
(
    n_name VARCHAR(255),
    r_name VARCHAR(255),
    o_totalprice DECIMAL(18, 2)
);

INSERT INTO #temp_result (n_name, r_name, o_totalprice)
SELECT n_name, r_name, o_totalprice
FROM customer AS c
    JOIN orders AS o ON c.c_custkey = o.o_custkey
    JOIN nation AS n ON c.c_nationkey = n.n_nationkey
    JOIN region AS r ON n.n_regionkey = r.r_regionkey;

CREATE UNIQUE INDEX idx_temp_result ON #temp_result (n_name DESC, r_name ASC, o_totalprice DESC);

SELECT * FROM #temp_result;

-- REMORPH CLEANUP: DROP TABLE #temp_result;
-- REMORPH CLEANUP: DROP INDEX idx_temp_result ON #temp_result;
