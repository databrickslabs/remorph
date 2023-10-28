-- Should return True.
SELECT CONTAINS(COLLATE('ñn', 'sp'), COLLATE('n', 'sp'));
SELECT CONTAINS(COLLATE('ñn', 'sp'), 'n');