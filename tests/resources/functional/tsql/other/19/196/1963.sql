--Query type: DDL
IF EXISTS (SELECT * FROM sys.assemblies WHERE name = 'MyAssembly')
    DROP ASSEMBLY MyAssembly;
-- REMORPH CLEANUP: DROP ASSEMBLY MyAssembly;
