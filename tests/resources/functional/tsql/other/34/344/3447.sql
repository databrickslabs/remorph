--Query type: DCL
CREATE USER Clerk WITHOUT LOGIN;
GRANT IMPERSONATE ON USER::Clerk TO Clerk;
REVOKE IMPERSONATE ON USER::Clerk FROM Clerk;
SELECT *
FROM (
    VALUES ('DENY', 'IMPERSONATE', 'Clerk')
) AS permissions(state_desc, permission_name, principal_name);
-- REMORPH CLEANUP: DROP USER Clerk;