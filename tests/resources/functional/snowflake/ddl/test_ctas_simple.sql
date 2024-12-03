-- snowflake sql:
CREATE TABLE employee as SELECT employee_id, name FROM employee_stage;

-- databricks sql:
CREATE TABLE employee as SELECT employee_id, name FROM employee_stage;
