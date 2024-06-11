-- ## CHECKSUM_AGG
--
-- There is no direct equivalent of CHECKSUM_AGG in Databricks SQL. The following
-- conversion is a suggestion and may not be perfectly functional.

-- tsql sql:
SELECT CHECKSUM_AGG(col1) FROM t1;

-- databricks sql:
SELECT MD5(CONCAT_WS(',', COLLECT_LIST(col1))) FROM t1;
