-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/opendatasource-transact-sql?view=sql-server-ver16

SELECT *  
FROM OPENDATASOURCE('SQLNCLI',  
    'Data Source=London\Payroll;Integrated Security=SSPI')  
    .AdventureWorks2022.HumanResources.Employee;