-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

-- Or, create an EXTERNAL FILE FORMAT and an EXTERNAL TABLE

--Create external file format
CREATE EXTERNAL FILE FORMAT DemoFileFormat
WITH (
 FORMAT_TYPE=PARQUET
)
GO

--Create external table:
CREATE EXTERNAL TABLE tbl_TaxiRides(
 vendorID VARCHAR(100) COLLATE Latin1_General_BIN2,
 tpepPickupDateTime DATETIME2,
 tpepDropoffDateTime DATETIME2,
 passengerCount INT,
 tripDistance FLOAT,
 puLocationId VARCHAR(8000),
 doLocationId VARCHAR(8000),
 startLon FLOAT,
 startLat FLOAT,
 endLon FLOAT,
 endLat FLOAT,
 rateCodeId SMALLINT,
 storeAndFwdFlag VARCHAR(8000),
 paymentType VARCHAR(8000),
 fareAmount FLOAT,
 extra FLOAT,
 mtaTax FLOAT,
 improvementSurcharge VARCHAR(8000),
 tipAmount FLOAT,
 tollsAmount FLOAT,
 totalAmount FLOAT
)
WITH (
 LOCATION = 'yellow/puYear=*/puMonth=*/*.parquet',
 DATA_SOURCE = NYCTaxiExternalDataSource,
 FILE_FORMAT = MyFileFormat\.\./\.\./\.\./azure-sql/
);
GO

--Then, query the data via an external table with T-SQL:
SELECT TOP 10 *
FROM tbl_TaxiRides;
GO