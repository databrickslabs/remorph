--Query type: DDL
SELECT * FROM (VALUES ('db2', 'Standard', 512, 'S3')) AS db_properties (name, edition, maxsize, service_objective);