-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-xml-index-selective-xml-indexes?view=sql-server-ver16

CREATE XML INDEX filt_sxi_index_c  
ON Tbl(xmlcol)  
USING XML INDEX sxi_index  
FOR ( pathabc );