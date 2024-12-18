-- tsql sql:
IF (SELECT snapshot_isolation_state FROM (VALUES ('TPCH_DATABASE', 0)) AS sys_databases (name, snapshot_isolation_state) WHERE name = 'TPCH_DATABASE') = 0
BEGIN
    ALTER DATABASE TPCH_DATABASE SET ALLOW_SNAPSHOT_ISOLATION ON;
END;
