--Query type: DQL
WITH session_info AS ( SELECT 'session_context' AS context_info, 1 AS session_id ) SELECT context_info FROM session_info WHERE session_id = ( SELECT @@SPID );