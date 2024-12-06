-- tsql sql:
CREATE EVENT SESSION tpch_session
ON SERVER
ADD EVENT sqlserver.sql_batch_completed,
ADD EVENT sqlserver.sql_batch_starting
ADD TARGET package0.etw_classic_sync_target
(
SET default_etw_session_logfile_path = N'C:\tpch\traces\tpch.etl'
)
WITH (
MAX_MEMORY = 8MB,
MAX_EVENT_SIZE = 8MB
);
