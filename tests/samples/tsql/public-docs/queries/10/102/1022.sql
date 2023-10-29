-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql?view=sql-server-ver16

CREATE INDEX IX_VendorID ON ProductVendor (VendorID);
CREATE INDEX IX_VendorID ON dbo.ProductVendor (VendorID DESC, Name ASC, Address DESC);
CREATE INDEX IX_VendorID ON Purchasing..ProductVendor (VendorID);