-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-xml-index-transact-sql?view=sql-server-ver16

IF EXISTS (SELECT name FROM sys.indexes
            WHERE name = N'IXML_ProductModel_CatalogDescription_Path')
    DROP INDEX IXML_ProductModel_CatalogDescription_Path
        ON Production.ProductModel;  
GO  
CREATE XML INDEX IXML_ProductModel_CatalogDescription_Path
    ON Production.ProductModel (CatalogDescription)
    USING XML INDEX PXML_ProductModel_CatalogDescription FOR PATH ;
GO