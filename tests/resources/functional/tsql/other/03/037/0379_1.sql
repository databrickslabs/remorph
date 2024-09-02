--Query type: DML
INSERT INTO awards WITH (TABLOCK) (award_id, award_description)
SELECT *
FROM (
    VALUES (1, 'Best Employee'),
           (2, 'Best Manager'),
           (3, 'Best Team')
) AS DataFile (award_id, award_description);