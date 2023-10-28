TRUNCATE TABLE source_table;

TRUNCATE TABLE target_table;

INSERT INTO source_table (ID, description) VALUES
    (50, 'This is a duplicate in the source and has no match in target'),
    (50, 'This is a duplicate in the source and has no match in target')
    ;