--Query type: DQL
WITH temp_result AS (
    SELECT CAST('<root><a>1</a></root>' AS XML) AS c3,
           1 AS c1,
           2 AS c2
)
SELECT c1,
       c2,
       c3
FROM temp_result
WHERE c3.exist('/root[@a=sql:column("c1")]' ) = 1
