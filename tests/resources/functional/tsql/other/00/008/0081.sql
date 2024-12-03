--Query type: DDL
CREATE TABLE applications (app_name sysname);
INSERT INTO applications (app_name) VALUES ('my_new_app');
DECLARE @app_name sysname;
SELECT @app_name = app_name FROM applications;
EXEC sp_addrolemember 'db_owner', @app_name;
SELECT * FROM applications;
-- REMORPH CLEANUP: DROP TABLE applications;
