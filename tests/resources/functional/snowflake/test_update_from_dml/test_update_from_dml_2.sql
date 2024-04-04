
-- snowflake sql:
UPDATE target
                            SET v = b.v
                            FROM (SELECT k, MIN(v) v FROM src GROUP BY k) b
                            WHERE target.k = b.k;

-- databricks sql:
MERGE INTO target USING (SELECT k, MIN(v) AS v FROM src GROUP BY k) AS b ON target.k = b.k WHEN MATCHED THEN UPDATE SET v = b.v  ;
