-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-as-select-transact-sql?view=sql-server-ver16

-- Example is based on AdventureWorks
CREATE EXTERNAL TABLE hdfsCustomer
    WITH (
            LOCATION = '/pdwdata/customer.tbl',
            DATA_SOURCE = customer_ds,
            FILE_FORMAT = customer_ff
            ) AS

SELECT *
FROM dimCustomer;
GO