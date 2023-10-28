CREATE OR REPLACE TABLE base64_table (v VARCHAR, base64_string VARCHAR);
INSERT INTO base64_table (v) VALUES ('HELLO');
UPDATE base64_table SET base64_string = BASE64_ENCODE(v);