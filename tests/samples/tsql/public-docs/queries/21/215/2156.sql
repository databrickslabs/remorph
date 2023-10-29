-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-xml-index-transact-sql?view=sql-server-ver16

IF EXISTS (SELECT * FROM sys.indexes
            WHERE name = N'PXML_ProductModel_CatalogDescription')
    DROP INDEX PXML_ProductModel_CatalogDescription
        ON Production.ProductModel;  
GO  
CREATE PRIMARY XML INDEX PXML_ProductModel_CatalogDescription
    ON Production.ProductModel (CatalogDescription)
    WITH (XML_COMPRESSION = ON);  
GO