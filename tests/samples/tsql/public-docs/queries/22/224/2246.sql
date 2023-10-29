-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql?view=sql-server-ver16

REBUILD WITH
(
  XML_COMPRESSION = OFF ON PARTITIONS (1),
  XML_COMPRESSION = ON ON PARTITIONS (2, 4, 6 TO 8),
  XML_COMPRESSION = OFF ON PARTITIONS (3, 5)
);