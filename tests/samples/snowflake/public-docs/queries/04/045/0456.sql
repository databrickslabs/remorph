-- see https://docs.snowflake.com/en/sql-reference/functions/json_extract_path_text

CREATE TABLE demo1 (id INTEGER, json_data VARCHAR);
INSERT INTO demo1 SELECT
   1, '{"level_1_key": "level_1_value"}';
INSERT INTO demo1 SELECT
   2, '{"level_1_key": {"level_2_key": "level_2_value"}}';
INSERT INTO demo1 SELECT
   3, '{"level_1_key": {"level_2_key": ["zero", "one", "two"]}}';