--Query type: DCL
DECLARE @username sysname;
SELECT @username = username
FROM (
    VALUES ('JohnDoe')
) AS usernames(username);
ALTER AUTHORIZATION ON SERVER::[SalesServer2] TO [@username];
