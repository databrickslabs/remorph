-- see https://docs.snowflake.com/en/sql-reference/functions/extract_semantic_categories

USE ROLE data_engineer;

SELECT EXTRACT_SEMANTIC_CATEGORIES('my_db.my_schema.hr_data', 5000);