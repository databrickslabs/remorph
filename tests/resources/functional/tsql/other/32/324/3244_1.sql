--Query type: DCL
SELECT 'DROP LOGIN ' + l.login + ';' AS login_drop, 'DROP USER ' + u.[user] + ';' AS [user_drop]
FROM (
    VALUES ('login1'),
           ('login2')
) l (login)
CROSS JOIN (
    VALUES ('user1'),
           ('user2')
) u ([user]);