-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql-identity-property?view=sql-server-ver16

-- Here is the generic syntax for finding identity value gaps in data.
-- The illustrative example starts here.
SET IDENTITY_INSERT tablename ON;

DECLARE @minidentval column_type;
DECLARE @maxidentval column_type;
DECLARE @nextidentval column_type;

SELECT @minidentval = MIN($IDENTITY),
    @maxidentval = MAX($IDENTITY)
FROM tablename

IF @minidentval = IDENT_SEED('tablename')
    SELECT @nextidentval = MIN($IDENTITY) + IDENT_INCR('tablename')
    FROM tablename t1
    WHERE $IDENTITY BETWEEN IDENT_SEED('tablename')
            AND @maxidentval
        AND NOT EXISTS (
            SELECT *
            FROM tablename t2
            WHERE t2.$IDENTITY = t1.$IDENTITY + IDENT_INCR('tablename')
            )
ELSE
    SELECT @nextidentval = IDENT_SEED('tablename');

SET IDENTITY_INSERT tablename OFF;

-- Here is an example to find gaps in the actual data.
-- The table is called img and has two columns: the first column
-- called id_num, which is an increasing identification number, and the
-- second column called company_name.
-- This is the end of the illustration example.
-- Create the img table.
-- If the img table already exists, drop it.
-- Create the img table.
IF OBJECT_ID('dbo.img', 'U') IS NOT NULL
    DROP TABLE img;
GO

CREATE TABLE img (
    id_num INT IDENTITY(1, 1),
    company_name SYSNAME
);

INSERT img (company_name)
VALUES ('New Moon Books');

INSERT img (company_name)
VALUES ('Lucerne Publishing');

-- SET IDENTITY_INSERT ON and use in img table.
SET IDENTITY_INSERT img ON;

DECLARE @minidentval SMALLINT;
DECLARE @nextidentval SMALLINT;

SELECT @minidentval = MIN($IDENTITY)
FROM img

IF @minidentval = IDENT_SEED('img')
    SELECT @nextidentval = MIN($IDENTITY) + IDENT_INCR('img')
    FROM img t1
    WHERE $IDENTITY BETWEEN IDENT_SEED('img')
            AND 32766
        AND NOT EXISTS (
            SELECT *
            FROM img t2
            WHERE t2.$IDENTITY = t1.$IDENTITY + IDENT_INCR('img')
            )
ELSE
    SELECT @nextidentval = IDENT_SEED('img');

SET IDENTITY_INSERT img OFF;