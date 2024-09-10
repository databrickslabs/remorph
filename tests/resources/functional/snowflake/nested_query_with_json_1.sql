-- snowflake sql:
SELECT
  A.COL1,
  A.COL2,
  B.COL3,
  B.COL4
FROM
  (
    SELECT COL1, COL2
    FROM VALUES
      ('val1', 'val2'),
      ('val3', 'val4')
    AS A(COL1, COL2)
  ) A,
  (
  SELECT * FROM
   ( SELECT PARSE_JSON(COL5):PRICE::FLOAT AS COL3, COL4
    FROM VALUES
      ('{"PRICE": 100.50}', 'val1'),
      ('{"PRICE": 200.75}', 'val3')
    AS B(COL5, COL4)
   )
  ) B
WHERE
  A.COL1 = B.COL4;

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
  FROM VALUES
    ('val1', 'val2'),
    ('val3', 'val4') AS A(COL1, COL2)
) AS A, (
  SELECT
    *
  FROM (
    SELECT
      CAST(FROM_JSON(COL5, schema_of_json('{COL5}')).PRICE AS DOUBLE) AS COL3,
      COL4
    FROM VALUES
      ('{"PRICE": 100.50}', 'val1'),
      ('{"PRICE": 200.75}', 'val3') AS B(COL5, COL4)
  )
) AS B
WHERE
  A.COL1 = B.COL4

-- experimental sql:
SELECT
  A.COL1,
  A.COL2,
  B.COL3,
  B.COL4
from
  (
    SELECT
      COL1,
      COL2
    FROM
    VALUES
      ('val1', 'val2'),
      ('val3', 'val4') AS A (COL1, COL2)
  ) as A,
  (
  SELECT * FROM
    (SELECT
      CAST (PARSE_JSON (COL5).price AS DOUBLE) AS COL3,
      COL4
    FROM
    VALUES
      ('{"price": 100.50}', 'val1'),
      ('{"price": 200.75}', 'val3') AS B (COL5, COL4))
  ) AS B
WHERE
  A.col1 = B.col4