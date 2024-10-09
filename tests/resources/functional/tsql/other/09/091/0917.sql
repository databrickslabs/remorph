--Query type: DDL
CREATE DATABASE SCOPED CREDENTIAL [NewCredential]
WITH IDENTITY = 'new_username',
      SECRET = 'new_password';
-- REMORPH CLEANUP: DROP DATABASE SCOPED CREDENTIAL [NewCredential];