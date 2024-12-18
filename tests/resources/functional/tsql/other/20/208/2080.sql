-- tsql sql:
EXEC sp_set_session_context 'user_id', 4; SELECT value AS user_id FROM (VALUES (SESSION_CONTEXT(N'user_id'))) AS user_id_context(value);
