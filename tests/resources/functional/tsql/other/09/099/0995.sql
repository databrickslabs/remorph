-- tsql sql:
CREATE ASSEMBLY myExternalLibrary
FROM 'https://example.com/myExternalLibrary_v2.2.zip'
WITH PERMISSION_SET = SAFE;
-- REMORPH CLEANUP: DROP ASSEMBLY myExternalLibrary;
