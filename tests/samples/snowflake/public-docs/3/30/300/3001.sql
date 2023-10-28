CREATE MATERIALIZED VIEW emp_view
    AS
    SELECT id "Employee Number", lname "Last Name", location "Home Base" FROM emp;