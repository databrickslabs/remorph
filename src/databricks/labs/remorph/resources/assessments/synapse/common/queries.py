class SynapseQueries:
    @staticmethod
    def list_databases() -> str:
        """Get list of databases"""
        return """
               SELECT
                   NAME,
                   DATABASE_ID,
                   CREATE_DATE,
                   STATE,
                   STATE_DESC,
                   COLLATION_NAME
               FROM SYS.DATABASES WHERE NAME <> 'master' ;
               """

    @staticmethod
    def list_tables() -> str:
        """Get list of tables"""
        return """
               SELECT
                   TABLE_CATALOG,
                   TABLE_SCHEMA,
                   TABLE_NAME,
                   TABLE_TYPE
               FROM INFORMATION_SCHEMA.TABLES ;
               """

    @staticmethod
    def list_columns() -> str:
        """Get list of columns"""
        return """
               SELECT
                   TABLE_CATALOG,
                   TABLE_SCHEMA,
                   TABLE_NAME,
                   COLUMN_NAME,
                   ORDINAL_POSITION,
                   COLUMN_DEFAULT,
                   IS_NULLABLE,
                   DATA_TYPE,
                   CHARACTER_MAXIMUM_LENGTH,
                   CHARACTER_OCTET_LENGTH,
                   NUMERIC_PRECISION,
                   NUMERIC_PRECISION_RADIX,
                   NUMERIC_SCALE,
                   DATETIME_PRECISION,
                   CHARACTER_SET_CATALOG,
                   CHARACTER_SET_SCHEMA,
                   CHARACTER_SET_NAME,
                   COLLATION_CATALOG,
                   COLLATION_SCHEMA,
                   COLLATION_NAME,
                   DOMAIN_CATALOG,
                   DOMAIN_SCHEMA,
                   DOMAIN_NAME
               FROM INFORMATION_SCHEMA.COLUMNS ;
               """

    @staticmethod
    def list_views(redact_sql_text: bool = False) -> str:
        """Get list of views"""
        return """
               SELECT
                   TABLE_CATALOG,
                   TABLE_SCHEMA,
                   TABLE_NAME,
                   CHECK_OPTION,
                   IS_UPDATABLE,
                   '[REDACTED]' as VIEW_DEFINITION
               FROM INFORMATION_SCHEMA.VIEWS
               """

    @staticmethod
    def list_routines(redact_sql_text: bool = False) -> str:
        """Get list of routines (functions + procedures)"""
        return """
                   SELECT
                       ROUTINE_CATALOG,
                       ROUTINE_SCHEMA,
                       ROUTINE_NAME,
                       ROUTINE_TYPE,
                       DATA_TYPE,
                       CHARACTER_MAXIMUM_LENGTH,
                       NUMERIC_PRECISION,
                       NUMERIC_SCALE,
                       DATETIME_PRECISION,
                       ROUTINE_BODY,
                       IS_DETERMINISTIC,
                       SQL_DATA_ACCESS,
                       IS_NULL_CALL,
                       '[REDACTED]' as ROUTINE_DEFINITION
                   FROM information_schema.routines
                   """

    @staticmethod
    def list_sessions(last_login_time: str | None = None) -> str:
        """Get session list with transformed login names and client IDs"""
        base_query = """
                     WITH session_data AS (
                         SELECT
                             *,
                             CURRENT_TIMESTAMP as extract_ts
                         FROM SYS.DM_PDW_EXEC_SESSIONS
                         WHERE CHARINDEX('system', LOWER(LOGIN_NAME)) = 0
                             {login_time_filter}
                     ),
                          login_transformed AS (
                              SELECT
                                  *,
                                  CASE
                                      WHEN LOWER(LOGIN_NAME) LIKE '%@%.%' THEN 'APP'
                                      ELSE 'USER'
                                      END as login_user_type,
                                  CASE
                                      WHEN LOWER(LOGIN_NAME) LIKE '%@%.%' THEN
                                          CASE
                                              WHEN PATINDEX('%@%', LOGIN_NAME) > 0 THEN
                                                  SUBSTRING(LOGIN_NAME, 1, PATINDEX('%@%', LOGIN_NAME) - 1)
                                              ELSE 'otherApp'
                                              END
                                      ELSE 'otherUser'
                                      END as login_user
                              FROM session_data
                          )
                     SELECT
                         *,
                         HASHBYTES('SHA2_256', login_user) as login_user_sha2,
                         HASHBYTES('SHA2_256', CAST(client_id AS VARCHAR)) as client_id_sha2
                     FROM login_transformed
                     """

        login_time_filter = f"AND login_time > '{last_login_time}'" if last_login_time else ""
        return base_query.format(login_time_filter=login_time_filter)

    @staticmethod
    def list_requests(min_end_time: str | None = None) -> str:
        """Get session request list with command type classification"""
        base_query = """
                              SELECT
                                  *,
                                  CASE
                                      WHEN UPPER(TRIM(SUBSTRING(command, 1, CHARINDEX(' ', command + ' ') - 1))) IN ('SELECT', 'WITH') THEN 'QUERY'
                                      WHEN UPPER(TRIM(SUBSTRING(command, 1, CHARINDEX(' ', command + ' ') - 1))) IN ('INSERT', 'UPDATE', 'MERGE', 'DELETE', 'TRUNCATE', 'COPY', 'IF', 'BEGIN', 'DECLARE', 'BUILDREPLICATEDTABLECACHE') THEN 'DML'
                                      WHEN UPPER(TRIM(SUBSTRING(command, 1, CHARINDEX(' ', command + ' ') - 1))) IN ('CREATE', 'DROP', 'ALTER') THEN 'DDL'
                                      WHEN UPPER(TRIM(SUBSTRING(command, 1, CHARINDEX(' ', command + ' ') - 1))) IN ('EXEC', 'EXECUTE') THEN 'ROUTINE'
                                      WHEN UPPER(TRIM(SUBSTRING(command, 1, CHARINDEX(' ', command + ' ') - 1))) = 'BEGIN'
                                          AND UPPER(TRIM(SUBSTRING(command, CHARINDEX(' ', command) + 1, CHARINDEX(' ', command + ' ', CHARINDEX(' ', command) + 1) - CHARINDEX(' ', command) - 1))) IN ('TRAN', 'TRANSACTION') THEN 'TRANSACTION_CONTROL'
                                      WHEN UPPER(TRIM(SUBSTRING(command, 1, CHARINDEX(' ', command + ' ') - 1))) = 'END'
                                          AND UPPER(TRIM(SUBSTRING(command, CHARINDEX(' ', command) + 1, CHARINDEX(' ', command + ' ', CHARINDEX(' ', command) + 1) - CHARINDEX(' ', command) - 1))) IN ('TRAN', 'TRANSACTION') THEN 'TRANSACTION_CONTROL'
                                      WHEN UPPER(TRIM(SUBSTRING(command, 1, CHARINDEX(' ', command + ' ') - 1))) IN ('COMMIT', 'ROLLBACK') THEN 'TRANSACTION_CONTROL'
                                      ELSE 'OTHER'
                                      END as command_type,
                                  CURRENT_TIMESTAMP as extract_ts,
                                  {command_redaction}
                            FROM SYS.DM_PDW_EXEC_REQUESTS
                            WHERE start_time IS NOT NULL
                            AND command IS NOT NULL
                            {end_time_filter}
                     """

        end_time_filter = f"AND end_time > '{min_end_time}'" if min_end_time else ""
        command_redaction = "'[REDACTED]' as command"

        return base_query.format(end_time_filter=end_time_filter, command_redaction=command_redaction).strip().rstrip(';')

    @staticmethod
    def get_db_storage_info() -> str:
        """Get database storage information"""
        return """
               SELECT *, CURRENT_TIMESTAMP AS EXTRACT_TS
               FROM (
                        SELECT
                            PDW_NODE_ID AS NODE_ID,
                            (SUM(RESERVED_PAGE_COUNT) * 8) / 1024 AS RESERVEDSPACEMB,
                            (SUM(USED_PAGE_COUNT)  * 8) / 1024 AS USEDSPACEMB
                        FROM SYS.DM_PDW_NODES_DB_PARTITION_STATS
                        GROUP BY PDW_NODE_ID
                    ) X
               """

    @staticmethod
    def get_table_storage_info() -> str:
        """Get detailed table storage information"""
        return """
               SELECT
                   OBJECT_SCHEMA_NAME(P.OBJECT_ID) AS SCHEMA_NAME,
                   OBJECT_NAME(P.OBJECT_ID) AS TABLE_NAME,
                   I.NAME AS INDEX_NAME,
                   I.TYPE_DESC AS INDEX_TYPE,
                   P.ROWS AS ROW_COUNT,
                   P.DATA_COMPRESSION_DESC AS COMPRESSION_TYPE,
                   AU.TOTAL_PAGES * 8.0 / 1024 AS TOTAL_SIZE_MB,
                   AU.USED_PAGES * 8.0 / 1024 AS USED_SIZE_MB,
                   CURRENT_TIMESTAMP AS EXTRACT_TS
               FROM SYS.PARTITIONS P
                        INNER JOIN SYS.INDEXES I ON P.OBJECT_ID = I.OBJECT_ID AND P.INDEX_ID = I.INDEX_ID
                        INNER JOIN SYS.ALLOCATION_UNITS AU ON P.PARTITION_ID = AU.CONTAINER_ID
               WHERE P.OBJECT_ID > 255
               ORDER BY AU.TOTAL_PAGES DESC
               """

    @staticmethod
    def get_query_performance_stats(days: int = 7) -> str:
        """Get query performance statistics"""
        return f"""
            SELECT
                qs.EXECUTION_COUNT,
                QS.TOTAL_ELAPSED_TIME / 1000000.0 AS TOTAL_ELAPSED_TIME_SEC,
                QS.TOTAL_WORKER_TIME / 1000000.0 AS TOTAL_WORKER_TIME_SEC,
                QS.TOTAL_LOGICAL_READS,
                QS.TOTAL_PHYSICAL_READS,
                QS.TOTAL_LOGICAL_WRITES,
                QS.LAST_EXECUTION_TIME,
                QS.CREATION_TIME,
                QS.LAST_ELAPSED_TIME / 1000000.0 AS LAST_ELAPSED_TIME_SEC,
                QS.LAST_WORKER_TIME / 1000000.0 AS LAST_WORKER_TIME_SEC,
                QS.LAST_LOGICAL_READS,
                QS.LAST_PHYSICAL_READS,
                QS.LAST_LOGICAL_WRITES,
                QS.TOTAL_ROWS,
                QS.LAST_ROWS,
                QS.MIN_ROWS,
                QS.MAX_ROWS,
                QS.STATEMENT_START_OFFSET,
                QS.STATEMENT_END_OFFSET,
                CURRENT_TIMESTAMP as EXTRACT_TS
            FROM SYS.DM_EXEC_QUERY_STATS QS
            WHERE QS.last_execution_time >= DATEADD(day, -{days}, GETDATE())
            ORDER BY QS.total_elapsed_time DESC
        """
