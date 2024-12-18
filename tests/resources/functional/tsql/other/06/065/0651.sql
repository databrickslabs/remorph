-- tsql sql:
INSERT INTO aggr (k, v)
SELECT *
FROM (
    VALUES (2, 20), (2, 20), (2, 25), (2, 30)
) AS temp_result (k, v);
