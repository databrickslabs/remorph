-- see https://docs.snowflake.com/en/sql-reference/functions/contains

-- Should return True.
SELECT CONTAINS(COLLATE('ñn', 'sp'), COLLATE('n', 'sp'));
SELECT CONTAINS(COLLATE('ñn', 'sp'), 'n');