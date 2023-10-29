-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table-column

CREATE TABLE t(x INT);
INSERT INTO t VALUES (1), (2), (3);
ALTER TABLE t ADD COLUMN y INT DEFAULT 100;
INSERT INTO t(x) VALUES (4), (5), (6);

ALTER TABLE t ALTER COLUMN y DROP DEFAULT;