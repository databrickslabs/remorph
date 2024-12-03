--Query type: DQL
SELECT FORMATMESSAGE('Unsigned int %u, %u', v1, v2) FROM (VALUES (50, -50)) AS t(v1, v2);
