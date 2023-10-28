CREATE OR REPLACE TABLE i (id NUMBER, col1 NUMBER, col2 NUMBER);
INSERT INTO i (id, col1, col2) VALUES 
    (1, 0, 5), 
    (2, 0, null), 
    (3, null, 5), 
    (4, null, null);