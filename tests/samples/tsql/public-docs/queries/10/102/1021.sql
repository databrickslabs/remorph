-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql?view=sql-server-ver16

CREATE INDEX IX_ProductVendor_VendorID
  ON ProductVendor (VendorID);