-- snowflake sql:
SELECT A.COL1, A.COL2, B.COL3, B.COL4 FROM
                            (SELECT COL1, COL2 FROM TABLE1) A,
                            (SELECT VALUE:PRICE::FLOAT AS COL3, COL4 FROM
                            (SELECT * FROM TABLE2 ) AS K
                            ) B
                            WHERE A.COL1 = B.COL4;

-- databricks sql:
SELECT
  A.COL1,
  A.COL2,
  B.COL3,
  B.COL4
FROM (
  SELECT
    COL1,
    COL2
  FROM TABLE1
) AS A, (
  SELECT
    CAST(VALUE:PRICE AS DOUBLE) AS COL3,
    COL4
  FROM (
    SELECT
      *
    FROM TABLE2
  ) AS K
) AS B
WHERE
  A.COL1 = B.COL4;

