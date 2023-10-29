-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-type-transact-sql?view=sql-server-ver16

CREATE TYPE InventoryItem AS TABLE
(
	[Name] NVARCHAR(50) NOT NULL,
	SupplierId BIGINT NOT NULL,
	Price DECIMAL (18, 4) NULL,
	PRIMARY KEY (
		Name
	),
	INDEX IX_InventoryItem_Price (
		Price
	)
)
GO