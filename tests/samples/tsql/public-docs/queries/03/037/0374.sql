-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-login-transact-sql?view=sql-server-ver16

-- run this to retrieve the password hash for an individual Login:
SELECT LOGINPROPERTY('Andreas','PASSWORDHASH') AS password_hash;
-- as an alternative, the catalog view sys.sql_logins can be used to retrieve the password hashes for multiple accounts at once. (This could be used to create a dynamic sql statemnt from the result set)
SELECT name, password_hash
FROM sys.sql_logins
  WHERE
    principal_id > 1    -- excluding sa
    AND
    name NOT LIKE '##MS_%##' -- excluding special MS system accounts
-- create the new SQL Login on the new database server using the hash of the source server
CREATE LOGIN Andreas
  WITH PASSWORD = 0x02000A1A89CD6C6E4C8B30A282354C8EA0860719D5D3AD05E0CAE1952A1C6107A4ED26BEBA2A13B12FAB5093B3CC2A1055910CC0F4B9686A358604E99BB9933C75B4EA48FDEA HASHED;