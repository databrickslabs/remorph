-- see https://docs.snowflake.com/en/sql-reference/operators-logical

CREATE TABLE logical (t BOOLEAN, f BOOLEAN, n BOOLEAN);
INSERT INTO logical (t, f, n) VALUES (True, False, NULL);