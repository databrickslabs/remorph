MERGE INTO target USING (select k, max(v) as v from src group by k) AS b ON target.k = b.k
  WHEN MATCHED THEN UPDATE SET target.v = b.v
  WHEN NOT MATCHED THEN INSERT (k, v) VALUES (b.k, b.v);