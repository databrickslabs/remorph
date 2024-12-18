-- tsql sql:
CREATE EXTERNAL TABLE [dbo].[all_lineitem]
(
    [l_orderkey] INT NOT NULL,
    [l_partkey] INT NOT NULL,
    [l_suppkey] INT NOT NULL,
    [l_linenumber] INT NOT NULL,
    [l_quantity] DECIMAL(12, 2) NOT NULL,
    [l_extendedprice] DECIMAL(12, 2) NOT NULL,
    [l_discount] DECIMAL(12, 2) NOT NULL,
    [l_tax] DECIMAL(12, 2) NOT NULL,
    [l_returnflag] CHAR(1) NOT NULL,
    [l_linestatus] CHAR(1) NOT NULL,
    [l_shipdate] DATE NOT NULL,
    [l_commitdate] DATE NOT NULL,
    [l_receiptdate] DATE NOT NULL,
    [l_shipinstruct] CHAR(25) NOT NULL,
    [l_shipmode] CHAR(10) NOT NULL,
    [l_comment] VARCHAR(44) NOT NULL
)
WITH (
    DATA_SOURCE = MyExtSrc,
    SCHEMA_NAME = 'dbo',
    OBJECT_NAME = 'lineitem',
    DISTRIBUTION = ROUND_ROBIN
);
-- REMORPH CLEANUP: DROP EXTERNAL TABLE [dbo].[all_lineitem];
