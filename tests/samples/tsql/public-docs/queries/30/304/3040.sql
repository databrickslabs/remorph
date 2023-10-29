-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/json-modify-transact-sql?view=sql-server-ver16

UPDATE Employee
SET jsonCol=JSON_MODIFY(jsonCol,'$.info.address.town','London')
WHERE EmployeeID=17