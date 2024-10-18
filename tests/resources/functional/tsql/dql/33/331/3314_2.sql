--Query type: DQL
SELECT @@IDENTITY AS last_identity_value
FROM (
    VALUES (1)
) AS temp_result(dummy);