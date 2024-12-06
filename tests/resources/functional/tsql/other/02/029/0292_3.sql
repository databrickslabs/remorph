-- tsql sql:
INSERT INTO array_test (ID, array1, array2, tip)
SELECT ID, array1, array2, tip
FROM (
    VALUES (1, '<a><i>101</i><i>null</i><i>102</i></a>', '<a><i>null</i><i>103</i><i>null</i></a>', 'NULLs overlap')
) AS temp_result_set (ID, array1, array2, tip);

SELECT *
FROM array_test;
