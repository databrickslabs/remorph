-- snowflake sql:
select emp_id from abc.emp where emp_id = $ids;

-- databricks sql:
select emp_id from abc.emp where emp_id = $ids;