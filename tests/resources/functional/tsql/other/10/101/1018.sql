--Query type: DDL
CREATE FUNCTION dbo.ByteLength (@input_string NVARCHAR(4000)) RETURNS INT AS BEGIN DECLARE @byte_length INT; SELECT @byte_length = LEN(@input_string) * 2; RETURN (@byte_length); END;
