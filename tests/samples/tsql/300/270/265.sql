INSERT OPENQUERY (MyLinkServer, 
    'SELECT Name, GroupName 
     FROM AdventureWorks2022.HumanResources.Department')  
VALUES ('Environmental Impact', 'Engineering');  
GO