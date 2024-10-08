-- snowflake sql:
SELECT A.COL1, B.COL2 FROM TABL1 A JOIN TABL2 B ON (A.COL1 = B.COL1 OR (A.COL1 IS NULL AND B.COL1 IS NULL));

-- databricks sql:
SELECT
  A.COL1,
  B.COL2
FROM TABL1 AS A
JOIN TABL2 AS B
  ON (
    A.COL1 = B.COL1 OR (
      A.COL1 IS NULL AND B.COL1 IS NULL
    )
  );
