-- snowflake sql:
CREATE OR REPLACE TABLE employee as SELECT employee_id, name FROM employee_stage;

-- databricks sql:
CREATE OR REPLACE TABLE employee as SELECT employee_id, name FROM employee_stage;
