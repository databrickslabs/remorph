--Query type: DQL
SELECT IDENT_CURRENT('t7') AS CurrentIdentity FROM (VALUES (1)) AS dummy(row);