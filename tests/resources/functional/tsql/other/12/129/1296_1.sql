--Query type: DML
ALTER TABLE #example_table NOCHECK CONSTRAINT salary_cap;
INSERT INTO #example_table (id, name, salary)
SELECT id, name, salary
FROM (
    VALUES (3, 'Pat Jones', 105000)
) AS temp_result (id, name, salary);
ALTER TABLE #example_table CHECK CONSTRAINT salary_cap;
