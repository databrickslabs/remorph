--Query type: DML
INSERT INTO sequence_demo (dummy) SELECT dummy FROM (VALUES ('temp_dummy')) AS temp_result (dummy);