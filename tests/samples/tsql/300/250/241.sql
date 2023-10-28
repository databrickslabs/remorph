-- Specify the remote data source using a four-part name   
-- in the form linked_server.catalog.schema.object.  
  
DELETE MyLinkServer.AdventureWorks2022.HumanResources.Department 
WHERE DepartmentID > 16;  
GO