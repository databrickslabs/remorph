-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-fulltext-index-transact-sql?view=sql-server-ver16

CREATE FULLTEXT INDEX ON Production.Document (
    Title LANGUAGE 1033,
    DocumentSummary LANGUAGE 1033,
    Document TYPE COLUMN FileExtension LANGUAGE 1033
) KEY INDEX PK_Document_DocumentID
WITH STOPLIST = SYSTEM,
    SEARCH PROPERTY LIST = DocumentPropertyList,
    CHANGE_TRACKING OFF,
    NO POPULATION;
GO