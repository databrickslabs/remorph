-- see https://docs.snowflake.com/en/sql-reference/functions/check_json

CREATE TABLE sample_json_table (ID INTEGER, varchar1 VARCHAR, variant1 VARIANT);
INSERT INTO sample_json_table (ID, varchar1) VALUES 
    (1, '{"ValidKey1": "ValidValue1"}'),
    (2, '{"Malformed -- Missing value": }'),
    (3, NULL)
    ;
UPDATE sample_json_table SET variant1 = varchar1::VARIANT;