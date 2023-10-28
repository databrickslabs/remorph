CREATE TABLE non_null_counter(col1 INTEGER, col2 INTEGER);
INSERT INTO non_null_counter(col1, col2) VALUES
    (NULL, NULL),   -- all NULL values
    (NULL, 1),      -- one NULL value
    (1, NULL),      -- one NULL value
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);