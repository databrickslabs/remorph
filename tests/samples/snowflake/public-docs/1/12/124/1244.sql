CREATE OR REPLACE TABLE like_ex(subject varchar(20));
INSERT INTO like_ex VALUES
    ('John  Dddoe'),
    ('Joe   Doe'),
    ('John_down'),
    ('Joe down'),
    ('Elaine'),
    (''),    -- empty string
    (null);