--Query type: DDL
CREATE FUNCTION dbo.get_order_length (@order_status NVARCHAR(4000)) RETURNS INT AS BEGIN DECLARE @len INT SET @len = (SELECT TOP 1 {fn BIT_LENGTH(o_orderstatus)} FROM (VALUES ('O'), ('F')) AS orders(o_orderstatus)) RETURN (@len) END
