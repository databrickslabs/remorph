--Query type: DML
INSERT INTO aggr (id, value, other_value)
SELECT id, value, other_value
FROM (
    VALUES (1, 10, NULL)
) AS temp (id, value, other_value);
