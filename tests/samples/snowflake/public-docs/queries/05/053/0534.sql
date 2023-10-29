-- see https://docs.snowflake.com/en/sql-reference/sql/insert

CREATE TABLE t1 (v VARCHAR);

-- works as expected.
INSERT INTO t1 (v) VALUES
   ('three'),
   ('four');

-- Fails with error "Numeric value 'd' is not recognized"
-- even though the data type of 'd' is the same as the
-- data type of the column v.
INSERT INTO t1 (v) VALUES
   (3),
   ('d');