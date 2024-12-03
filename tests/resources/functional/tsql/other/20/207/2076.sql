--Query type: DCL
EXEC('SELECT IPAddress, Username, Password FROM (VALUES ("xxx.xxx.xxx.xxx", "domain1\backupuser", "*****")) AS temp(IPAddress, Username, Password);');
