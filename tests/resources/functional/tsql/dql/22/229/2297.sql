--Query type: DQL
WITH asymmetric_key_properties AS (SELECT 256 AS key_id)
SELECT ASYMKEYPROPERTY(key_id, 'algorithm_desc') AS Encryption_Algorithm,
       ASYMKEYPROPERTY(key_id, 'string_sid') AS String_Security_ID,
       ASYMKEYPROPERTY(key_id, 'sid') AS Security_ID
FROM asymmetric_key_properties
