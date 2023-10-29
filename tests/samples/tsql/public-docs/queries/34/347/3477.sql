-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/xml-schema-namespace?view=sql-server-ver16

USE AdventureWorks;  
GO  
SELECT xml_schema_namespace(N'production',N'ProductDescriptionSchemaCollection');  
GO