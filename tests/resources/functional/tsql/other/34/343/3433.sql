-- tsql sql:
CREATE SYMMETRIC KEY MyNewKey
    WITH ALGORITHM = AES_256
    ENCRYPTION BY PASSWORD = 'password123';

CREATE TABLE #temp
(
    name sysname,
    symmetric_key_id int,
    key_length int,
    algorithm nvarchar(50)
);

INSERT INTO #temp
SELECT * FROM sys.symmetric_keys;

GRANT ALTER ON SYMMETRIC KEY::MyNewKey TO JohnD;

SELECT * FROM #temp;

-- REMORPH CLEANUP:
DROP SYMMETRIC KEY MyNewKey;
DROP TABLE #temp;
