-- see https://docs.snowflake.com/en/sql-reference/sql/desc-view

CREATE VIEW emp_view AS SELECT id "Employee Number", lname "Last Name", location "Home Base" FROM emp;