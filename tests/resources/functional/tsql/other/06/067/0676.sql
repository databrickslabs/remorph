--Query type: DML
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'like_ex_new')
CREATE TABLE like_ex_new (
    subject_new VARCHAR(255)
);

INSERT INTO like_ex_new (subject_new)
SELECT subject_new FROM (
    VALUES ('200 times'), ('2000 times'), ('200%')
) AS temp (subject_new);

SELECT * FROM like_ex_new;

-- REMORPH CLEANUP: DROP TABLE like_ex_new;
