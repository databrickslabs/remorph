-- see https://docs.snowflake.com/en/sql-reference/constructs/join

CREATE OR REPLACE TABLE d1 (
  id number,
  name string
  );
INSERT INTO d1 (id, name) VALUES
  (1,'a'),
  (2,'b'),
  (4,'c');
CREATE OR REPLACE TABLE d2 (
  id number,
  value string
  );
INSERT INTO d2 (id, value) VALUES
  (1,'xx'),
  (2,'yy'),
  (5,'zz');
SELECT *
    FROM d1 NATURAL INNER JOIN d2
    ORDER BY id;