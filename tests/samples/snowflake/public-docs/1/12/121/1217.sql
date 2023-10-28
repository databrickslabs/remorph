CREATE OR REPLACE TABLE replace_example(subject varchar(10), pattern varchar(10), replacement varchar(10));
INSERT INTO replace_example VALUES('snowman', 'snow', 'fire'), ('sad face', 'sad', 'happy');

SELECT subject, pattern, replacement, REPLACE(subject, pattern, replacement) AS new FROM replace_example;
