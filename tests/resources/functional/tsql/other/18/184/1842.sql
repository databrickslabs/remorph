-- tsql sql:
DECLARE @myvar1 BIGINT = NEXT VALUE FOR my_sequence;
DECLARE @myvar2 BIGINT;
SET @myvar2 = NEXT VALUE FOR my_sequence;
DECLARE @myvar3 BIGINT = NEXT VALUE FOR my_sequence;
SELECT @myvar1 AS myvar1, @myvar2 AS myvar2, @myvar3 AS myvar3;
