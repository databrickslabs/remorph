--Query type: DCL
CREATE TABLE #sql_logins
(
    name sysname,
    password_hash varbinary(256),
    is_policy_checked bit,
    is_expiration_checked bit
);

INSERT INTO #sql_logins (name, password_hash, is_policy_checked, is_expiration_checked)
VALUES ('JohnDoe', 0x1234567890abcdef, 0, 0);

CREATE LOGIN JohnDoe
WITH PASSWORD = 'P@ssw0rd123!';

WITH LoginInfo AS
(
    SELECT name, password_hash, is_policy_checked, is_expiration_checked
    FROM #sql_logins
    WHERE name = 'JohnDoe'
)
SELECT *
FROM LoginInfo;

SELECT *
FROM #sql_logins
WHERE name = 'JohnDoe';

-- REMORPH CLEANUP: DROP TABLE #sql_logins;
-- REMORPH CLEANUP: DROP LOGIN JohnDoe;
