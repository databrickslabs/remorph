--Query type: DDL
IF NOT EXISTS (SELECT * FROM sys.master_files WHERE name = 'TestFile')
BEGIN
    ALTER DATABASE AdventureWorks2022
    ADD FILE
    (
        NAME = TestFile,
        FILENAME = N'c:\testfile.ndf'
    );
END

ALTER DATABASE AdventureWorks2022
MODIFY FILE
(
    NAME = TestFile,
    FILENAME = N'c:\testfile.ndf'
);

SELECT *
FROM (
    VALUES (
        1, 'Item 1', 10.99),
        (2, 'Item 2', 5.99),
        (3, 'Item 3', 7.99)
    ) AS Items (ItemID, ItemName, Price);
-- REMORPH CLEANUP: DROP DATABASE AdventureWorks2022;
