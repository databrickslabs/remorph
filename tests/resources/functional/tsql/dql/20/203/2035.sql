--Query type: DQL
SELECT CONVERT(nvarchar(16), CAST(GETDATE() AS time), 0) AS TimeStyle0, CONVERT(nvarchar(16), CAST(GETDATE() AS time), 121) AS TimeStyle121, CONVERT(nvarchar(32), CAST(GETDATE() AS datetime2), 0) AS Datetime2Style0, CONVERT(nvarchar(32), CAST(GETDATE() AS datetime2), 121) AS Datetime2Style121 FROM (VALUES (1)) AS t2(c3);
