-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/node-id-from-parts-transact-sql?view=sql-server-ver16

INSERT INTO Person($node_id, ID, [name])
SELECT NODE_ID_FROM_PARTS(OBJECT_ID('Person'), ID) as node_id, ID, [name]
FROM OPENROWSET (BULK 'person_0_0.csv',
    DATA_SOURCE = 'staging_data_source',
    FORMATFILE = 'format-files/person.xml',
    FORMATFILE_DATA_SOURCE = 'format_files_source',
    FIRSTROW = 2) AS staging_data;
;