--Query type: DQL
SELECT LEAST(T1.val1, T1.val2, T1.val3) AS LeastVal
FROM (
    VALUES ('6.62', 3.1415, N'7')
) AS T1(val1, val2, val3);