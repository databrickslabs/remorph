--Query type: DCL
PRINT 'The database maintenance tasks have been completed successfully.';
SELECT *
FROM (
    VALUES ('Task 1'), ('Task 2'), ('Task 3')
) AS Tasks (TaskName);