--Query type: DDL
CREATE TABLE #temp_table
(
    login_sname SYSNAME DEFAULT SUSER_SNAME(),
    employee_id UNIQUEIDENTIFIER DEFAULT NEWID(),
    login_date DATETIME DEFAULT GETDATE()
);

WITH temp_result AS
(
    SELECT SUSER_SNAME() AS login_sname,
           NEWID() AS employee_id,
           GETDATE() AS login_date
)
INSERT INTO #temp_table (login_sname, employee_id, login_date)
SELECT login_sname, employee_id, login_date
FROM temp_result;
