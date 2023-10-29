-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-fulltext-index-transact-sql?view=sql-server-ver16

CREATE FULLTEXT CATALOG production_catalog;
GO

CREATE FULLTEXT INDEX ON Production.ProductReview (
    ReviewerName LANGUAGE 1033,
    EmailAddress LANGUAGE 1033,
    Comments LANGUAGE 1033
) KEY INDEX PK_ProductReview_ProductReviewID ON production_catalog;
GO