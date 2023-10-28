USE ROLE data_engineer;

CREATE OR REPLACE TABLE classification_results(v VARIANT) AS
  SELECT EXTRACT_SEMANTIC_CATEGORIES('my_db.my_schema.hr_data');