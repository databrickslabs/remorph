--Query type: DCL
CREATE ROLE CustomerService;
CREATE ROLE MarketingDepartment;
REVOKE VIEW DEFINITION ON ROLE::CustomerService FROM MarketingDepartment CASCADE;
SELECT * FROM sys.database_principals WHERE name IN ('CustomerService', 'MarketingDepartment');
