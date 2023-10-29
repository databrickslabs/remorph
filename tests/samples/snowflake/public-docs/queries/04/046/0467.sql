-- see https://docs.snowflake.com/en/sql-reference/functions/to_double

CREATE TABLE double_demo (d DECIMAL(7, 2), v VARCHAR, o VARIANT);
INSERT INTO double_demo (d, v, o) SELECT 1.1, '2.2', TO_VARIANT(3.14);
SELECT TO_DOUBLE(d), TO_DOUBLE(v), TO_DOUBLE(o) FROM double_demo;