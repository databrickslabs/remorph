-- tsql sql:
CREATE PARTITION FUNCTION pf_date (datetime) AS RANGE RIGHT FOR VALUES ('20000101', '20010101');
CREATE PARTITION SCHEME ps_date AS PARTITION pf_date ALL TO ('PRIMARY');
CREATE TABLE [dbo].[Sales_out]
(
    [date] datetime,
    [product] varchar(50),
    [store] varchar(50),
    [quantity] int,
    [price] decimal(10, 2),
    [amount] money
)
ON ps_date ([date]);
INSERT INTO [dbo].[Sales_out] ([date], [product], [store], [quantity], [price])
VALUES ('20000101', 'ProductA', 'Store1', 10, 100.0), ('20010101', 'ProductB', 'Store2', 20, 200.0);
UPDATE [dbo].[Sales_out]
SET [amount] = ISNULL(CAST([quantity]*[price] AS MONEY),0);
SELECT * FROM [dbo].[Sales_out];
