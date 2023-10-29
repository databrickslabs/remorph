-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-selective-xml-indexes?view=sql-server-ver16

ALTER INDEX sxi_index  
ON Tbl  
PAD_INDEX = ON;