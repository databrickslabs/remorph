-- tsql sql:
DECLARE @python_path nvarchar(255) = 'C:\PythonExtension\pythonextension.zip';
DECLARE @dll_name nvarchar(255) = 'pythonextension.dll';
EXEC sp_addextendedproc 'sp_python', @dll_name;
CREATE TABLE python_extension (
    name nvarchar(255),
    path nvarchar(255)
);
INSERT INTO python_extension (name, path)
VALUES ('Python', @python_path);
SELECT * FROM python_extension;
-- REMORPH CLEANUP: DROP TABLE python_extension;
-- REMORPH CLEANUP: EXEC sp_dropextendedproc 'sp_python';
