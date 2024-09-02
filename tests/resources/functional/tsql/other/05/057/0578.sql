--Query type: DDL
WITH ExternalLibrary AS (
    SELECT 'customPackage' AS LibraryName,
           'C:\Path\To\customPackage.zip' AS CONTENT,
           'R' AS LANGUAGE
)
SELECT 'ALTER EXTERNAL LIBRARY ' + LibraryName + ' SET (CONTENT = ''' + CONTENT + ''') WITH (LANGUAGE = ''' + LANGUAGE + ''');' AS AlterLibraryStatement
FROM ExternalLibrary;